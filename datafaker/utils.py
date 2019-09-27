#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import functools
import os
import json
import re
import time

from datafaker.compat import safe_decode, safe_encode, compat_open
from datafaker.constant import STR_TYPES, INT_TYPES, FLOAT_TYPES
from datafaker.drivers import load_sqlalchemy
from datafaker.exceptions import FileNotFoundError
from datafaker.reg import reg_keyword, reg_cmd, reg_args, reg_integer, reg_int, reg_all_int


def save2file(items, outfile):
    """
    将数据保存到文件
    :param items:
    :param outfile:
    :param spliter:
    :return:
    """
    with open(outfile, 'a+') as fp:
        fp.writelines(items)


def save2db(items, table, schema, connect, batch_size):
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
    names_format = u"(" + u",".join(formats) + u")"
    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    column_names = ','.join(names)
    i = 0
    for batch in batches:
        batch_value = []
        for row in batch:
            batch_value.append(names_format % tuple(row))

        sql = u"insert into {table} ({column_names}) values {values}".format(
            table=table, column_names=column_names, values=u','.join([item for item in batch_value]))
        session.execute(sql)
        i += batch_size
        session.commit()

    session.close()


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
    with compat_open(filepath, 'r', encoding='UTF-8') as fp:
        lines = fp.read().splitlines()
        # start with # is comment line, and filter empty line
        lines = [safe_decode(line) for line in lines if line and not line.startswith("#") and line.strip()]
    return lines


def diffdate(date1, date2):
    """
    #计算两个日期相差天数，自定义函数名，和两个日期的变量名。
    :param date1:
    :param date2:
    :return:
    """
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')

    return (date2-date1).days


def process_op_args(arg, lst_name):
    """
    解析op标记的参数
    将c12*c2+c22 解析成 columns[12]*columns[2]+columns[22]
    
    :param arg: 
    :param lst_name: 
    :return: 
    """
    digits = sorted(reg_all_int(arg), reverse=True)

    for digit in digits:
         arg = arg.replace('c%d' % digit, 'c[%d]' % digit)
    arg = arg.replace('c', lst_name)

    return arg
