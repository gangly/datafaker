#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datafaker.dbs.rdbdb import RdbDB
from datafaker.drivers import load_sqlalchemy


class HiveDB(RdbDB):

    def construct_self_rows(self):
        session = load_sqlalchemy(self.args.connect)
        sql = 'desc %s' % self.args.table
        rows = session.execute(sql)
        rows = [row for row in rows]
        return rows
