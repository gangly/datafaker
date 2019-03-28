#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.utils import json_item


def test_json_item():
    list1 = ['name', 'age']
    list2 = ['mary', 12]

    assert '''{"name":"mary", "age":12}''' == json_item(list1, list2)