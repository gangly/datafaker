#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from datafaker.compat import safe_encode
from datafaker.constant import JSON_FORMAT, TEXT_FORMAT
from datafaker.dbs.basedb import BaseDB
from datafaker.utils import save2file, json_item


class FileDB(BaseDB):

    def construct_self_rows(self):
        return []

    def save_data(self, lines):
        spliter = self.args.outspliter if self.args.outspliter else ','
        filepath = os.path.join(self.args.connect, self.args.table)

        items = []
        if self.args.format == TEXT_FORMAT:

            for item in lines:
                line = spliter.join([str(safe_encode(word)) for word in item]) + "\n"
                items.append(line)
        else:
            items = [line+"\n" for line in lines]
        save2file(items, filepath)

