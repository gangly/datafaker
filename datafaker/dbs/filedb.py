#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.dbs.basedb import BaseDB
from datafaker.utils import save2file


class FileDB(BaseDB):

    def construct_self_rows(self):
        return []

    def save_data(self, lines):
        spliter = self.args.outspliter if self.args.outspliter else ','
        save2file(lines, self.args.outfile, spliter)

