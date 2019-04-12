#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from datafaker.constant import ES_INDEX_MAX_ROWS
from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParamError


class EsDB(BaseDB):

    def init(self):
        self.es = Elasticsearch(self.args.connect.split(','))

    def construct_self_rows(self):
        raise ParamError('es must set meta parameter')

    def save_data(self, lines):
        index_type = self.args.format if self.args.format else 'json'
        actions = []
        i = 0
        length = len(lines)
        for line in lines:
            source = dict(zip(self.column_names, line))
            action = {
                "_index": self.args.table,
                "_type": index_type,
                "_source": source,
            }
            actions.append(action)
            i = i+1
            if i % ES_INDEX_MAX_ROWS == 0 or i >= length:
                success, _ = bulk(self.es, actions, index=self.args.table, raise_on_error=True)
                print('insert %d actions' % i)
