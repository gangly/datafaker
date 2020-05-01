#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.constant import STR_TYPES
from datafaker.dbs.basedb import BaseDB
from datafaker.drivers import load_sqlalchemy


class RdbDB(BaseDB):

    def init(self):
        self.session = load_sqlalchemy(self.args.connect)

    def save_data(self, lines):

        names = [column['name'] for column in self.schema]
        ctypes = [column['ctype'] for column in self.schema]

        # 构造数据格式，字符串需要加上单引号
        formats = ["'%s'" if ctype in STR_TYPES else "%s" for ctype in ctypes]
        names_format = u"(" + u",".join(formats) + u")"
        column_names = ','.join(names)

        if self.args.connect.lower().startswith('oracle'):
            self.save_oracle(lines, names_format, column_names)
        else:
            self.save_other_rdb(lines, names_format, column_names)

    def save_other_rdb(self, lines, names_format, column_names):
        """
        其实数据库，多条同时写入
        :param lines:
        :param names_format:
        :param column_names:
        :return:
        """
        batch_value = []
        for row in lines:
            batch_value.append(names_format % tuple(row))

        sql = u"insert into {table} ({column_names}) values {values}".format(
            table=self.args.table, column_names=column_names, values=u','.join([item for item in batch_value]))
        self.session.execute(sql)

        self.session.commit()

    def save_oracle(self, lines, names_format, column_names):
        """
        oracle中数据不能多条同时写入
        :param lines:
        :param names_format:
        :param column_names:
        :return:
        """

        for row in lines:
            sql = u"insert into {table} ({column_names}) values {values}".format(
                table=self.args.table, column_names=column_names, values=names_format % tuple(row))
            self.session.execute(sql)

        self.session.commit()




