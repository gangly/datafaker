#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import os
import json
import time

from datafaker.compat import safe_decode, safe_encode
from datafaker.constant import RDB_BATCH_SIZE, STR_TYPES, INT_TYPES, FLOAT_TYPES
from datafaker.drivers import load_sqlalchemy
from datafaker.exceptions import FileNotFoundError
from datafaker.reg import reg_keyword, reg_cmd, reg_args


def save2file(items, outfile):
    """
    将数据保存到文件
    :param items:
    :param outfile:
    :param spliter:
    :return:
    """
    with open(outfile, 'w') as fp:
        fp.writelines(items)


def save2db(items, table, schema, connect):
    """
    保存数据到mysql, hive
    :param items: 保存的数据，list
    :param table: 表名
    :param schema: 表shema
    :param connect: 数据库连接信息
    :return:
    """
    session = load_sqlalchemy(connect)

    names = [column['name'] for column in schema]
    ctypes = [column['ctype'] for column in schema]

    # 构造数据格式，字符串需要加上单引号
    formats = ["'%s'" if ctype in STR_TYPES else "%s" for ctype in ctypes]
    names_format = "(" + ",".join(formats) + ")"
    batches = [items[i:i + RDB_BATCH_SIZE] for i in range(0, len(items), RDB_BATCH_SIZE)]
    column_names = ','.join(names)
    for batch in batches:
        batch_value = []
        for row in batch:
            batch_value.append(names_format % tuple(row))
        sql = u"insert into {table} ({column_names}) values {values}".format(
            table=table, column_names=column_names, values=','.join([item for item in batch_value]))
        session.execute(sql)
    session.commit()


def json_item(column_names, item):
    map = dict(zip(column_names, item))
    return json.dumps(map)


def count_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        now = time.time()
        timeused = float((now - start))
        print('time used: %.3f s' % timeused)
        return ret
    return wrapper


def read_file_lines(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    with open(filepath) as fp:
        lines = fp.read().splitlines()
        # start with # is comment line, and filter empty line
        lines = [line for line in lines if line and not line.startswith("#") and line.strip()]
    return lines
