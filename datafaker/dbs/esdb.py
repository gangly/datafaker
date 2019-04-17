#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from datafaker.constant import ES_BATCH_SIZE
from datafaker.dbs.basedb import BaseDB
from datafaker.exceptions import ParamError


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
        i = 0
        length = len(lines)
        for line in lines:
            source = dict(zip(self.column_names, line))
            action = {
                "_index": self.index,
                "_type": self.type,
                "_source": source,
            }
            actions.append(action)
            i = i+1
            if i % ES_BATCH_SIZE == 0 or i >= length:
                success, _ = bulk(self.es, actions, index=self.args.table, raise_on_error=True)
                print('insert %d actions' % i)


