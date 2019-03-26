#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from faker import Factory


fake = Factory().create('zh_CN')
li = dir(fake)
def get_dir_run():
    with open('somefile.txt', 'wt') as f:
        for i in li:
            a = None
            try:
                cmd = "fake."+i+"()"
                a = eval(cmd)
                print(cmd)
            except Exception:
                a = None
            if a:
                message = "{0}   # {1} \n".format(cmd,a)
                f.write(message)

def test_func():
    print(fake.random_number(1))
    print(fake.random_number(2))
    print(fake.random_number(3))

    print(fake.pydecimal(left_digits=None, right_digits=None, positive=True))
    print(fake.date())

    print(fake.date_between(2, 5))
    print(fake.date_time())
    print(fake.time())

