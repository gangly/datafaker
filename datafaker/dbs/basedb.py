#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from abc import abstractmethod

from datafaker.compat import safe_encode, safe_decode
from datafaker.constant import INT_TYPES, FLOAT_TYPES
from datafaker.exceptions import MetaFileError, FileNotFoundError, EnumMustNotEmptyError, ParseSchemaError
from datafaker.fakedata import FackData
from datafaker.reg import reg_keyword, reg_cmd, reg_args
from datafaker.utils import save2file, count_time, read_file_lines
import os


class BaseDB(object):

    def __init__(self, args):
        self.args = args
        self.schema = self.parse_schema()
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
        lines = self.fake_data()
        spliter = self.args.out_spliter if self.args.out_spliter else ','
        if self.args.outprint:
            for items in lines:
                # line = spliter.join([str(item) for item in items])
                # for item in items:
                line = spliter.join([str(safe_encode(item)) for item in items])
                print(line)
        elif self.args.outfile:
            save2file(lines, self.args.outfile, spliter)
        else:
            self.save_data(lines)
        msg = 'printed' if self.args.outprint else 'saved'
        print("generated records : %d" % len(lines))
        print("%s records : %d" % (msg, len(lines)))

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
                if len(rets) == 1:
                    rets = read_file_lines(rets[0])

                if ctype in INT_TYPES:
                    args = [int(ret) for ret in rets]
                elif ctype in FLOAT_TYPES:
                    args = [float(ret) for ret in rets]
                else:
                    args = rets
            else:
                args = [int(ret) for ret in rets]


            # args = reg_args(keyword)
            item['cmd'] = cmd
            item['ctype'] = ctype
            item['args'] = args
            shema.append(item)

        return shema

    def construct_meta_rows(self):
        filepath = self.args.meta
        lines = read_file_lines(filepath)
        rows = []
        for line in lines:
            words = line.split("||")
            if len(words) != 3:
                raise ParseSchemaError('parse schema error, %s' % line)
            rows.append(words)
        return rows



    @abstractmethod
    def construct_self_rows(self):
        return []

    @abstractmethod
    def save_data(self, lines):
        pass
