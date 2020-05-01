#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParamError
from datafaker.utils import json_item


class EsDB(BaseDB):

    def init(self):
        auth = None
        if self.args.auth:
            auth = self.args.auth.split(':')
        self.es = Elasticsearch(self.args.connect.split(','), http_auth=auth)
        self.index, self.type = self.args.table.split('/')

    def construct_self_rows(self):
        raise ParamError('es must set meta parameter')

    def save_data(self, lines):
        actions = []

        for line in lines:

            source = self.format_data(line)
            action = {
                "_index": self.index,
                "_type": self.type,
                "_source": source,
            }
            actions.append(action)

        success, _ = bulk(self.es, actions, index=self.args.table, raise_on_error=True)

    def format_data(self, columns):
        if self.args.metaj:
            data = self.metaj_content % tuple(columns)
            source = json.loads(data)
        else:
            source = dict(zip(self.column_names, columns))
        return source





