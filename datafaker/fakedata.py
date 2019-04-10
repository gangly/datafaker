#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random

from faker import Faker


class FackData(object):

    def __init__(self, locale, start=0):

        self.faker = Faker(locale)
        self.faker.random_int()
        self.faker_funcs = dir(self.faker)
        self.id = start

    ######## mysql 数值类型 #############
    def fake_tinyint(self, *args):
        return self.faker.random_int(0, 255) if len(args) > 0 else self.faker.random_int(-128, 127)

    def fake_smallint(self, *args):
        return self.faker.random_int(0, 65535) if len(args) > 0 else self.faker.random_int(-32768, 32767)

    def fake_mediumint(self, *args):
        return self.faker.random_int(0, 16777215) if len(args) > 0 else self.faker.random_int(-8388608, 8388607)

    def fake_int(self, *args):
        return self.faker.random_int(0, 4294967295) if len(args) > 0 else self.faker.random_int(-2147483648, 2147483647)

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

    def fake_date(self, *args):
        """
        以今天为基点，start_day, end_day两个参数，往前后推的天数
        end_day默认今天
        :param args:
        :return:
        """
        return self.faker.date_between(*args)

    def fake_time(self, *args):
        return self.faker.time()

    def fake_year(self, *args):
        return self.faker.year()

    def fake_datetime(self, *args):
        return self.faker.date_time()

    def fake_timestamp(self, *args):

        return self.faker.unix_time()



    ########### mysql 字符串类型##############

    def fake_char(self, *args):
        return self.faker.pystr(min_chars=1, max_chars=255)

    def fake_varchar(self, *args):
        return self.faker.pystr(min_chars=1, max_chars=args[0])

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

    def fake_id(self, *args):
        """
        用于实现自增id
        :param args:
        :return:
        """
        self.id += 1
        return self.id

    def fake_enum(self, *args):
        """
        实现枚举类型，随机返回一个列表中值
        :param args:
        :return:
        """
        return random.choice(list(args))

    #################
    def do_fake(self, keyword, args):
        """
        首先查看是否在faker类的成员函数内，如果在则调用；
        否者调用FakeData类中自定义的成员函数
        :param keyword:
        :param args:
        :return:
        """
        if keyword in self.faker_funcs:
            method = getattr(self.faker, keyword, None)
        else:
            method = getattr(self, 'fake_' + keyword, None)
        if callable(method):
            return method(*args)
        return None

