#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.dbs.basedb import BaseDB
# from drivers import load_sqlalchemy
from datafaker.dbs.rdbdb import RdbDB
from datafaker.drivers import load_sqlalchemy
from datafaker.utils import save2db


class MysqlDB(RdbDB):

    def construct_self_rows(self):
        session = load_sqlalchemy(self.args.connect)
        sql = 'show full columns from %s' % self.args.table
        rows = session.execute(sql)
        return rows

