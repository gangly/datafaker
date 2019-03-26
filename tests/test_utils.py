#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from utils import get_table_schema, json_item


def test_get_table_schema():
    url = "mysql+mysqldb://root:root@localhost:3600/test"
    items = get_table_schema(url, 'stu')
    assert len(items) == 2
    assert items[0] == ('name', 'varchar(32)', 'student name')


def test_json_item():
    list1 = ['name', 'age']
    list2 = ['mary', 12]

    assert '''{"name":"mary", "age":12}''' == json_item(list1, list2)