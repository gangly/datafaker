#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from faker import Factory


fake = Factory().create('zh_CN')


def test_func():
    print(fake.random_number(1))
    print(fake.random_number(2))
    print(fake.random_number(3))

    print(fake.pydecimal(left_digits=None, right_digits=None, positive=True))
    print(fake.date())

    print(fake.date_between(2, 5))
    print(fake.date_time())
    print(fake.time())


def test_faker():
    print(fake.country_code())
    print(fake.district())
    print(fake.postcode())
    print(fake.street_suffix())
    print(fake.bs())
    print(fake.company())
    print(fake.company_prefix())
    print(fake.company_suffix())
    print(fake.job())

    print('-------internet-------------')

    print(fake.file_extension())
    print(fake.file_name())
    print(fake.file_path())
    print(fake.mime_type())
    print(fake.company_email())
    print(fake.domain_name())
    print(fake.email())
    print(fake.image_url())
    print(fake.ipv4())
    print(fake.ipv6())
    print(fake.mac_address())
    print(fake.tld())
    print(fake.uri())
    print(fake.url())
    print(fake.user_name())
    print(fake.user_agent())
    print(fake.linux_platform_token())
    print(fake.isbn10())
    print(fake.isbn13())

    print('-----------------')

    print(fake.credit_card_expire())
    print(fake.credit_card_full())
    print(fake.credit_card_number())
    print(fake.credit_card_provider())
    print(fake.credit_card_security_code())
    print(fake.currency_code())

    print('-----------------')
    print(fake.century())
    print(fake.date())
    print(fake.date_between())
    print(fake.date_this_month())
    print(fake.date_this_year())
    print(fake.date_time())
    print(fake.date_time_between())
    print(fake.month())
    print(fake.month_name())
    print(fake.time())
    print(fake.timezone())
    print(fake.unix_time())
    print(fake.year())

    print('-----text------------')

    # print(fake.paragraph())
    # print(fake.sentence())
    # print(fake.text())
    # print(fake.word())
    # print(fake.binary())
    print(fake.locale())
    print(fake.md5())
    print(fake.password())
    print(fake.sha1())
    print(fake.sha256())
    print(fake.uuid4())

    print('--------person----------')
    print(fake.phone_number())
    print(fake.phonenumber_prefix())
    print(fake.profile())
    print(fake.simple_profile())
    print(fake.ssn())

    print('--------number----------')
    print(fake.random_digit())
    print(fake.random_element())
    print(fake.random_letter())
    print(fake.random_number())
    print(fake.null_boolean())
    print(fake.boolean())
    print(fake.numerify())
    print(fake.color_name())
    print(fake.hex_color())
    print(fake.rgb_color())



