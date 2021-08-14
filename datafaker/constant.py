#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = '0.7.6'

# batch size for inserting records
BATCH_SIZE = 1000

# multiprocessing  queue, max size is 32767
MAX_QUEUE_SIZE = 30000

# time interval for streaming record producing
DEFAULT_INTERVAL = 1

# task num for paralleling
WORKERS = 4

# minimum records for multiple threading, single thread if number of record lower than MIN_RECORDS_FOR_PARALLEL
MIN_RECORDS_FOR_PARALLEL = 10

# output format
TEXT_FORMAT = 'text'
JSON_FORMAT = 'json'
DEFAULT_FORMAT = TEXT_FORMAT

# local language
DEFAULT_LOCALE = 'zh_CN'

# ENUM
ENUM_FILE = 'file://'

# types of needing quotation marks
STR_TYPES = ['date', 'time', 'datetime', 'char', 'varchar', 'tinyblob',
             'tinytext', 'text', 'mediumtext', 'longtext', 'string']


INT_TYPES = ['tinyint', 'smallint', 'mediumint', 'int', 'integer', 'bigint', ]

FLOAT_TYPES = ['float', 'double', 'decimal', ]




