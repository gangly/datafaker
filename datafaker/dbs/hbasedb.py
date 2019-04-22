#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParamError
import happybase

from datafaker.reg import reg_args


class HbaseDB(BaseDB):

    def init(self):
        host, port = self.args.connect.split(':')
        connection = happybase.Connection(host=host, port=int(port))
        self.table = connection.table(self.args.table)

    def construct_self_rows(self):
        raise ParamError('hbase must set meta parameter')

    def save_data(self, lines):
        with self.table.batch(batch_size=self.args.batch) as bt:
            args = reg_args(self.column_names[0])
            args = [int(arg) for arg in args]

            for line in lines:
                line = [str(word) for word in line]
                rowkey = line[0]
                if args:
                    words = [line[arg] for arg in args]
                    # words = [bytes((line[arg]).encode('utf-8')) for arg in args]
                    rowkey = u'_'.join(words)

                value = dict(zip(self.column_names[1:], line[1:]))
                # this put() will result in two mutations (two cells)
                bt.put(rowkey, value)



