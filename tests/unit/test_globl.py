#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datafaker import globl

globl.init()


def test_exists():
    assert False == globl.exists('aa')

    globl.set_value("aa", 10)
    assert True == globl.exists('aa')
