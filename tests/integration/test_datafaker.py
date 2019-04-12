#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys

from _pytest import tmpdir

from datafaker import main
from datafaker.cli import parse_args
from datafaker.testutils import FileCreator

META_CONTENT = """
   id||int||自增id[:id]
   name||varchar(20)||学生名字[:name]
   nickname||varchar(20)||学生名字[:enum(xiao ming, hah, lele, esd f222)]
   age||int||学生年龄[:enum(3, 6, 7, 8, 9)]
   age2||int||学生年龄[:age(10, 20)]
   score||decimal(4,2)||成绩[:decimal(4,2,0)]
   phone||varchar(20)||电话号码[:phone_number]
   email||decimal(4,2)||邮箱[:email]
   address||decimal(4,2)||地址[:address]
   """

def _main_file(cmd, meta=None):
    """
    以产生数据写到文件来集成测试
    :return:
    """

    if meta is None:
        meta = META_CONTENT

    sys.argv = cmd.strip().split(' ')
    args = parse_args()
    with open(args.meta, 'w') as fp:
        fp.write(meta)

    main()
    outfile = os.path.join(args.connect, args.table)
    with open(outfile) as fp:
        result = fp.read().splitlines()
    return result


def _main(cmd, meta=None):

    if meta is None:
        meta = META_CONTENT

    sys.argv = cmd.strip().split(' ')
    args = parse_args()
    with open(args.meta, 'w') as fp:
        fp.write(meta)
    main()


def _make_tmp_file():
    fc = FileCreator()
    test_tmpdir = fc.create_dir("testdata")
    meta_file = os.path.join(test_tmpdir, "schema.txt")
    return test_tmpdir, meta_file


def test_fake_data_to_file():

    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file {connect} hello.txt 10 --meta {meta_file}'.format(connect=test_tmpdir, meta_file=meta_file)
    result = _main_file(cmd)
    assert 10 == len(result)


def test_fake_data_to_file_with_header():

    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file {connect} hello.txt 10 --meta {meta_file} --withheader'.format(connect=test_tmpdir, meta_file=meta_file)

    result = _main_file(cmd)
    assert 11 == len(result)
    assert 'id,name,nickname,age,age2,score,phone,email,address' == result[0]


def test_fake_data_to_hbase():
    """
    must install hbase locally, and start thrift service
    :return:
    """
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file {connect} hello.txt 10 --meta {meta_file}'.format(connect=test_tmpdir, meta_file=meta_file)

    result = _main_file(cmd)
    assert 10 == len(result)