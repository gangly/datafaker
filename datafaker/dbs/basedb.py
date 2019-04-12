#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from abc import abstractmethod

from datafaker.compat import safe_encode, safe_decode
from datafaker.constant import INT_TYPES, FLOAT_TYPES, ENUM_FILE, JSON_FORMAT
from datafaker.exceptions import MetaFileError, FileNotFoundError, EnumMustNotEmptyError, ParseSchemaError
from datafaker.fakedata import FackData
from datafaker.reg import reg_keyword, reg_cmd, reg_args
from datafaker.utils import save2file, count_time, read_file_lines, json_item
import os


class BaseDB(object):

    def __init__(self, args):
        self.args = args
        self.schema = self.parse_schema()
        self.column_names = [item['name'] for item in self.schema]
        self.fakedata = FackData(self.args.locale)
        self.init()

    def init(self):
        pass

    def fake_data(self):
        lines = []
        for i in range(self.args.num):
            columns = self.fake_column()
            lines.append(columns)
        return lines

    def fake_column(self):
        columns = []
        for item in self.schema:
            columns.append(self.fakedata.do_fake(item['cmd'], item['args']))
        return columns

    @count_time
    def do_fake(self):
        data_items = self.fake_data()

        if self.args.format == JSON_FORMAT:
            data_items = [json_item(self.column_names, line) for line in data_items]

        data_num = len(data_items)
        spliter = self.args.outspliter if self.args.outspliter else ','

        if self.args.withheader and self.args.format != JSON_FORMAT:
            data_items.insert(0, self.column_names)

        if self.args.outprint:
            for items in data_items:
                if self.args.format != JSON_FORMAT:
                    line = spliter.join([str(safe_encode(item)) for item in items])
                    print(line)
                else:
                    print(items)
        elif self.args.outfile:
            save2file(data_items, self.args.outfile, spliter)
        else:
            self.save_data(data_items)
        msg = 'printed' if self.args.outprint else 'saved'
        print("generated records : %d" % data_num)
        print("%s records : %d" % (msg, data_num))

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
            if cmd == 'enum':
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
            else:
                args = [int(ret) for ret in rets]

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

