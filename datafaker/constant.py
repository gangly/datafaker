#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = '0.0.8'

# 每次插入mysql数据条数
BATCH_SIZE = 1000

# 判断哪些需要加上引号
STR_TYPES = ['date', 'time', 'datetime', 'char', 'varchar', 'tinyblob',
             'tinytext', 'text', 'mediumtext', 'longtext', 'string']


INT_TYPES = ['tinyint', 'smallint', 'mediumint', 'int', 'integer', 'bigint', ]

FLOAT_TYPES = ['float', 'double', 'decimal', ]