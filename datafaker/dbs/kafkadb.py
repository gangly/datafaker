#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from kafka import KafkaProducer
from datafaker.dbs.basedb import BaseDB
from datafaker.utils import json_item, count_time


class KafkaDB(BaseDB):

    def init(self):
        self.producer = KafkaProducer(bootstrap_servers=self.args.connect)

    def construct_self_rows(self):
        return []

    def save_data(self, content):
        self.producer.send(self.args.table, bytes(content.encode('utf-8')))


    # def save_data(self, lines):
    #     for line in lines:
    #         content = self.format_data(line)
    #         self.producer.send(self.args.table, bytes(content.encode('utf-8')))
    #         if self.args.interval:
    #             time.sleep(self.args.interval)

    @count_time
    def do_fake(self):
        i = 0
        try:
            while i < self.args.num:
                i += 1
                columns = self.fake_column(i)
                content = self.format_data(columns)
                if self.args.outprint:
                    print(content)
                self.save_data(content)
                print('insert %d records' % i)
                if self.args.interval:
                    time.sleep(self.args.interval)
        except KeyboardInterrupt:
            print("generated records : %d" % i)
            print("insert records : %d" % i)

    def format_data(self, columns):
        if self.args.metaj:
            data = self.metaj_content % tuple(columns)
        else:
            data = json_item(self.column_names, columns)

        return data