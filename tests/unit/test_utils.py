#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.utils import json_item, diffdate, process_op_args, read_file
import json


def test_json_item():
    list1 = ['name', 'age']
    list2 = ['mary', 12]

    assert json.loads('''{"name":"mary", "age":12}''') == json.loads(json_item(list1, list2))


def test_diff_date():
    assert 1 == diffdate('2019-04-14', '2019-04-15')


def test_process_op_args():
    assert 'columns[12]*columns[2]+columns[22]' == process_op_args('c12*c2+c22', 'columns')


def test_read_file():
    print(read_file('test_reg.py'))