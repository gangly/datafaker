#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import random
import time
from faker import Faker
from datafaker import compat
from datafaker.compat import Dict


class FackData(object):

    def __init__(self, locale):

        self.faker = Faker(locale)
        self.faker_funcs = dir(self.faker)
        self.lock = compat.Lock()
        self.auto_inc = Dict()
        self.current_num = 0

    ######## mysql 数值类型 #############

    def fake_tinyint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 255) if unsigned else self.faker.random_int(-128, 127)

    def fake_smallint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 65535) if unsigned else self.faker.random_int(-32768, 32767)

    def fake_mediumint(self, digits=None, unsigned=False):
        return self.faker.random_int(0, 16777215) if unsigned else self.faker.random_int(-8388608, 8388607)

    def fake_int(self, min=None, max=None, unsigned=False):
        if min or max:
            return self.faker.random_int(min, max)
        return self.faker.random_int(0, 4294967295) if unsigned else self.faker.random_int(-2147483648, 2147483647)

    def fake_integer(self, *args):
        return self.fake_int(*args)

    def fake_bigint(self, *args):
        return self.faker.random_int(0, 18446744073709551615) if len(args) > 0 \
            else self.faker.random_int(-9223372036854775808, 9223372036854775807)

    def fake_float(self, *args):
        return self.faker.pyfloat()

    def fake_double(self, *args):
        return self.fake_float()

    def fake_decimal(self, *args):
        """
        mysql中DECIMAL(6,2);
        最多可以存储6位数字，小数位数为2位; 因此范围是从-9999.99到9999.99

        而pyfloat left_digits, right_digits 表示小数点左右数字位数
        :param args:
        :return:
        """
        if len(args) >= 3:
            if int(args[2]) == 1:
                return self.faker.pyfloat(left_digits=(args[0] - args[1]), right_digits=args[1], positive=True)
            else:
                return -self.faker.pyfloat(left_digits=(args[0] - args[1]), right_digits=args[1], positive=True)
        return self.faker.pyfloat(left_digits=(args[0]-args[1]), right_digits=args[1])


    ############ mysql 日期和时间类型 ###################

    def fake_date(self, start_date='-30y', end_date='today', format='%Y-%m-%d'):
        """
        以今天为基点，start_day, end_day两个参数，往前后推的天数
        end_day默认今天
        format为输出格式
        :param args:
        :return:
        """

        thedate = self.faker.date_between(start_date, end_date)
        return thedate.strftime(format)

    def fake_date_between(self, start_date=None, end_date=None, format='%Y-%m-%d'):
        # 去掉时分秒，不然后续计算天差值会出错
        today = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d")
        today = datetime.datetime.strptime(today, '%Y-%m-%d')

        if start_date is None:
            start_diff = 'today'
        else:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            diff = (start_date - today).days
            start_diff = '%dd' % diff if diff != 0 else 'today'

        if end_date is None:
            end_diff = today
        else:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            diff = (end_date - today).days
            end_diff = '%dd' % diff if diff != 0 else 'today'

        return self.fake_date(start_diff, end_diff, format)

    def fake_time(self, *args):
        return self.faker.time()

    def fake_year(self, *args):
        return self.faker.year()

    def fake_datetime(self, now=0, format='%Y-%m-%d %H:%M:%S'):
        dt = datetime.datetime.now() if now else self.faker.date_time()
        return dt.strftime(format)

    def fake_timestamp(self, now=0):

        timestamp = int(time.time()) if now else self.faker.unix_time()
        return timestamp

    ########### mysql 字符串类型##############

    def fake_char(self, *args):
        return self.faker.pystr(min_chars=1, max_chars=255)

    def fake_varchar(self, max_chars=255):
        return self.faker.pystr(min_chars=1, max_chars=max_chars)

    def fake_tinyblob(self, *args):
        # TODO 待实现
        return None

    def fake_tinytext(self, *args):
        max_nb_chars = args[0] if len(args) else 255
        return self.faker.text(max_nb_chars=max_nb_chars)

    def fake_text(self, *args):
        max_nb_chars = args[0] if len(args) else 65535
        return self.faker.text(max_nb_chars=max_nb_chars)

    def fake_mediumtext(self, *args):
        # TODO 待实现
        return None

    def fake_longtext(self, *args):
        # TODO 待实现
        return None

    ############ hive 基本数据类型 #############

    def fake_number(self, digits=None, fix_len=0, positive=0):
        """
        digits=None, fix_len=0, positive=0

        :param digits:
        :param fix_len:
        :param positive:
        :return:
        """
        fixlen = (fix_len == 1)
        val = self.faker.random_number(digits=digits, fix_len=fixlen)
        if positive > 0:
            val = val if val >= 0 else -val
        if positive < 0:
            val = val if val <= 0 else -val
        return val

    def fake_string(self, *args):
        return self.faker.pystr(*args)

    ####### 定制函数 ##########
    def fake_age(self, *args):
        if not args:
            args = [0, 100]
        return self.faker.random_int(*args)

    def fake_inc(self, mark, start=0, step=1):
        """
        用于实现整型变量自增
        :param args:
        :return:
        """
        with self.lock:
            if mark not in self.auto_inc:
                self.auto_inc[mark] = int(start)
            ret = self.auto_inc[mark]
            self.auto_inc[mark] += int(step)
        return ret

    def fake_enum(self, *args):
        """
        实现枚举类型，随机返回一个列表中值
        :param args: 枚举数组
        :return:
        """
        return random.choice(list(args))

    def fake_order_enum(self, *args):
        """
        用于循环顺序产生枚举值。常用于多列关联产生值
        :param args: 数组值
        :return:
        """
        datas = list(args)
        num = len(datas)

        idx = (self.current_num % num) - 1
        return datas[idx]


    def fake_op(self, *args):
        """
        实现多字段四项运算
        :param args:
        :return:
        """
        return None

    ######## 执行主函数 #########
    def do_fake(self, keyword, args, current_num):
        """
        首先查看是否在faker类的成员函数内，如果在则调用；
        否者调用FakeData类中自定义的成员函数
        :param keyword:
        :param args:
        :return:
        """
        self.current_num = current_num
        method = getattr(self, 'fake_' + keyword, None)
        if callable(method):
            return method(*args)
        if keyword in self.faker_funcs:
            method = getattr(self.faker, keyword, None)
            if callable(method):
                return method(*args)
        return None
