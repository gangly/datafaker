#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from datafaker.constant import JSON_FORMAT
from datafaker.dbs.basedb import BaseDB
from datafaker.utils import save2file, json_item


class FileDB(BaseDB):

    def construct_self_rows(self):
        return []

    def save_data(self, lines):
        spliter = self.args.outspliter if self.args.outspliter else ','
        filepath = os.path.join(self.args.connect, self.args.table)

        save2file(lines, filepath, spliter)

