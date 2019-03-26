#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import os
import json
import time

from datafaker.compat import safe_decode, safe_encode
from datafaker.constant import BATCH_SIZE, STR_TYPES, INT_TYPES, FLOAT_TYPES
from datafaker.drivers import load_sqlalchemy
from datafaker.exceptions import FileNotFoundError
from datafaker.reg import reg_keyword, reg_cmd, reg_args


# def parse_table_schema_from_file(filepath):
#
#     if not os.path.exists(filepath):
#         raise FileNotFoundError
#     with open(filepath) as fp:
#         lines = fp.read().splitlines()
#         rows = [line.split("||") for line in lines]
#     return parse_table_schema_from_rows(rows)

#
# def get_table_schema(url, table):
#     """
#     获取表中字段信息
#     包括：字段名、字段类型、注释
#
#     mysql+pymysql://root:root@localhost:3600/test
#     hive://yarn@host:10000/default?auth=NONE
#     :param url: load_sqlalchemy 连接信息
#     :param table: 表名
#     :return: []
#     """
#     session = load_sqlalchemy(url)
#     if url.startswith('mysql'):
#         sql = 'show full columns from %s' % table
#     else:
#         sql = 'desc %s' % table
#     rows = session.execute(sql)
#     return parse_table_schema_from_rows(rows)


# def parse_table_schema_from_rows(rows):
#     shema = []
#     for row in rows:
#
#         # mysql show full columns command has more than three columns
#         # hive desc command has only three columns
#         item = {'name': row[0], 'type': row[1], 'comment': row[-1]}
#         keyword = reg_keyword(item['comment'])
#
#         ctype = reg_cmd(item['type'])
#         if not keyword:
#             keyword = item['type']
#
#         cmd = reg_cmd(keyword) if keyword else ctype
#
#         rets = reg_args(keyword)
#         if cmd == 'enum':
#             if ctype in INT_TYPES:
#                 args = [int(ret) for ret in rets]
#             elif ctype in FLOAT_TYPES:
#                 args = [float(ret) for ret in rets]
#             else:
#                 args = rets
#         else:
#             args = [int(ret) for ret in rets]
#
#         item['cmd'] = cmd
#         item['ctype'] = ctype
#         item['args'] = args
#         shema.append(item)
#
#     return shema


def make_sqlalchemy_uri(dbtype, host, port, db, user, password):
    "mysql+mysqldb://root:root@localhost:3600/test"
    if dbtype == 'mysql':
        uri = "mysql+mysqldb://root:root@localhost:3600/test"
    pass


def save2file(items, outfile, spliter=','):
    with open(outfile, 'w') as fp:
        lines = []
        for item in items:
            line = spliter.join([str(safe_encode(word)) for word in item]) + "\n"
            lines.append(line)

        fp.writelines(lines)


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
    batches = [items[i:i + BATCH_SIZE] for i in range(0, len(items), BATCH_SIZE)]
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
        lines = safe_decode(fp.read()).splitlines()
        lines = [line for line in lines if line and not line.startswith("#")]
    return lines
