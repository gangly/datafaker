#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.constant import HBASE_PUT_MAX_ROWS
from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParamError
import happybase
#
#
class HbaseDB(BaseDB):

    def init(self):
        host, port = self.args.connect.split(':')
        connection = happybase.Connection(host=host, port=int(port))
        self.table = connection.table(self.args.table)

    def construct_self_rows(self):
        raise ParamError('hbase must set meta parameter')

    def save_data(self, lines):
        with self.table.batch(batch_size=HBASE_PUT_MAX_ROWS) as b:
            for line in lines:
                line = [str(word) for word in line]
                value = dict(zip(self.column_names[1:], line[1:]))
                # this put() will result in two mutations (two cells)
                b.put(line[0], value)

                # self.table.put(line[0], value)

