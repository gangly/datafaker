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


def test_date_between():
    assert today.strftime('%Y-%m-%d') == fakedata.fake_date_between(start_date='2019-04-15', end_date='2019-04-15')
    assert fakedata.fake_date_between(start_date='2019-04-14', end_date='2019-04-15') in ['2019-04-14', '2019-04-15']
