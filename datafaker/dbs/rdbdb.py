#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.constant import STR_TYPES
from datafaker.dbs.basedb import BaseDB
from datafaker.drivers import load_sqlalchemy


class RdbDB(BaseDB):

    def init(self):
        self.session = load_sqlalchemy(self.args.connect)

    def __del__(self):
        self.session.close()

    def save_data(self, lines):

        names = [column['name'] for column in self.schema]
        ctypes = [column['ctype'] for column in self.schema]

        # 构造数据格式，字符串需要加上单引号
        formats = ["'%s'" if ctype in STR_TYPES else "%s" for ctype in ctypes]
        names_format = u"(" + u",".join(formats) + u")"
        column_names = ','.join(names)

        batch_value = []
        for row in lines:
            batch_value.append(names_format % tuple(row))

        sql = u"insert into {table} ({column_names}) values {values}".format(
            table=self.args.table, column_names=column_names, values=u','.join([item for item in batch_value]))
        self.session.execute(sql)

        self.session.commit()


