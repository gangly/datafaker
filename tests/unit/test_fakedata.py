#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime

from datafaker.constant import DEFAULT_LOCALE
from datafaker.fakedata import FackData

fakedata = FackData(DEFAULT_LOCALE)
today = datetime.date.today()


def test_date():
    print(fakedata.fake_date(start_date='today'))
    assert today.strftime('%Y-%m-%d') == fakedata.fake_date(start_date='today')
    assert today.strftime('%y%m%d') == fakedata.fake_date(start_date='today', format='%y%m%d')
    print(fakedata.fake_date('-5d', '-2d', '%Y-%m-%d %H:%M:%S'))


def test_date_between():
    assert today.strftime('%Y-%m-%d') == fakedata.fake_date_between(start_date='2019-04-15', end_date='2019-04-15')
    assert fakedata.fake_date_between(start_date='2019-04-14', end_date='2019-04-15') in ['2019-04-14', '2019-04-15']


def test_datetime_between():
    print(fakedata.fake_datetime_between('2019-04-14 00:00:00', '2019-04-15 00:00:00'))


def test_decimal():
    print()
    print(fakedata.fake_decimal(4, 2))
    print(fakedata.fake_decimal(4, 2, 1))
    print(fakedata.fake_decimal(4, 2, 0, 88, 90))
    print(fakedata.fake_decimal(4, 2, 0, -90, -88))
    assert fakedata.fake_decimal(4, 2, 1, 88, 90) > 88
