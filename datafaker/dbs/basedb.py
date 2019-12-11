#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from abc import abstractmethod
from time import sleep

from datafaker import compat
from datafaker.constant import INT_TYPES, FLOAT_TYPES, ENUM_FILE, JSON_FORMAT, MAX_QUEUE_SIZE, MIN_RECORDS_FOR_PARALLEL
from datafaker.exceptions import EnumMustNotEmptyError, ParseSchemaError
from datafaker.fakedata import FackData
from datafaker.reg import reg_keyword, reg_cmd, reg_args
from datafaker.utils import count_time, read_file_lines, json_item, process_op_args

class BaseDB(object):

    def __init__(self, args):
        self.args = args
        self.schema = self.parse_schema()
        self.column_names = [item['name'] for item in self.schema]
        self.fakedata = FackData(self.args.locale)

        self.queue = compat.Queue(maxsize=MAX_QUEUE_SIZE)
        self.isover = compat.Value('b', False)

        self.cur_num = compat.Value('L', 0)
        self.lock = compat.Lock()

        # 调用子类初始化函数
        self.init()

    def init(self):
        pass

    def get_cur_num(self):
        """
        必须将取值与计算同时锁住做原子计算，不然其他线程会执行产生多的数据
        :return:
        """
        with self.lock:
            self.cur_num.value += 1
            return self.cur_num.value-1

    def fake_data(self):
        """
        sleep是为了防止产生数据后消费数据过慢
        :return:
        """

        while self.get_cur_num() < self.args.num:
            columns = self.fake_column(self.cur_num.value)
            if self.args.format == JSON_FORMAT:
                columns = json_item(self.column_names, columns)
            self.queue.put(columns)

        sleep(0.1)
        self.isover.value = True

    def fake_column(self, current_num):
        columns = []
        for item in self.schema:
            columns.append(self.fakedata.do_fake(item['cmd'], item['args'], current_num))

        # 处理op操作，与多个字段有逻辑关系
        # 必须等第一遍完成后再处理一遍
        for idx, item in enumerate(self.schema):
            if item['cmd'] == 'op':
                columns[idx] = eval(item['args'][0])
        return columns

    @count_time
    def do_fake(self):

        if self.args.withheader and self.args.format != JSON_FORMAT:
            self.queue.put(self.column_names)

        procs = []
        # 如果产生的数据很少，则采用单线程
        procs_num = 1 if self.args.num <= MIN_RECORDS_FOR_PARALLEL else self.args.workers
        for _ in range(procs_num):
            producer = compat.Process(target=self.fake_data, args=())
            producer.daemon = True
            producer.start()
            procs.append(producer)

        func = self.print_data if self.args.outprint else self.save
        consumer = compat.Process(target=func, args=())
        consumer.daemon = True
        consumer.start()

        for proc in procs:
            proc.join()
        consumer.join()

    def save(self):
        saved_records = 0
        while not self.isover.value or not self.queue.empty():
            lines = []
            i = 0
            while i < self.args.batch and (not self.isover.value or not self.queue.empty()):
                try:
                    lines.append(self.queue.get_nowait())
                    i += 1
                except:
                    pass
            self.save_data(lines)
            if self.args.interval:
                time.sleep(self.args.interval)
            saved_records += len(lines)
            del(lines)
            print('insert %d records' % saved_records)

    def print_data(self):
        print('')
        # start with empty queue, must set self.isover.value
        while not self.isover.value or not self.queue.empty():
            try:
                data = self.queue.get_nowait()
                print(data)
                if self.args.interval:
                    time.sleep(self.args.interval)

            except:
                pass

    def parse_schema(self):
        if self.args.meta:
            schema = self.parse_meta_schema()
        else:
            schema = self.parse_self_schema()
        return schema

    def parse_self_schema(self):
        rows = self.construct_self_rows()
        return self.parse_schema_from_rows(rows)

    def parse_meta_schema(self):
        rows = self.construct_meta_rows()
        return self.parse_schema_from_rows(rows)

    def parse_schema_from_rows(self, rows):
        shema = []
        column_names = []
        for row in rows:
            item = {'name': row[0], 'type': row[1], 'comment': row[-1]}

            if item['name'] in column_names:
                raise ParseSchemaError('%s column has the same name' % item['name'])
            column_names.append(item['name'])

            keyword = reg_keyword(item['comment'])

            ctype = reg_cmd(item['type'])
            if not keyword:
                keyword = item['type']

            cmd = reg_cmd(keyword) if keyword else ctype

            rets = reg_args(keyword)
            if cmd == 'enum' or cmd == 'order_enum':
                if len(rets) == 0:
                    raise EnumMustNotEmptyError

                # 如果enum类型只有一个值，则产生固定值
                # 如果enum类型只有一个值，且以file://开头，则读取文件
                if len(rets) == 1 and rets[0].startswith(ENUM_FILE):
                    rets = read_file_lines(rets[0][len(ENUM_FILE):])

                if ctype in INT_TYPES:
                    args = [int(ret) for ret in rets]
                elif ctype in FLOAT_TYPES:
                    args = [float(ret) for ret in rets]
                else:
                    args = rets
            elif cmd in INT_TYPES:
                args = [int(ret) for ret in rets]
                args.append(True) if 'unsigned' in keyword else args.append(False)
            elif cmd == 'op':
                args = [process_op_args(rets[0], 'columns'), ]
            else:
                try:
                    args = [int(ret) for ret in rets]
                except:
                    args = rets

            item['cmd'] = cmd
            item['ctype'] = ctype
            item['args'] = args
            shema.append(item)

        return shema

    def construct_meta_rows(self):
        """
        元数据文件中每行中每个字段以||分割，一共有三列：
        第一列表示：字段名
        第二列表示：字段类型
        第三列表示：带标记的字段注释
        :return:
        """
        filepath = self.args.meta
        lines = read_file_lines(filepath)
        rows = []
        for line in lines:
            words = line.split("||")
            if len(words) != 3:
                raise ParseSchemaError('parse schema error, %s' % line)
            rows.append([word.strip() for word in words])
        return rows

    @abstractmethod
    def construct_self_rows(self):
        return []

    @abstractmethod
    def save_data(self, lines):
        pass

