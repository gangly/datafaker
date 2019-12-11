#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys

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


def test_fake_data_to_mysql():

    cmd = 'datafaker mysql mysql+mysqldb://root:root@localhost:3600/test student 100'
    sys.argv = cmd.strip().split(' ')
    main()

def test_fake_data_to_hbase():
    """
    must install hbase locally, and start thrift service
    :return:
    """
    meta_content = """
        ROWKEY(1)||varchar(20)||rowkey
        CF:FNUMBE||bigint||猪只编码[:number(18, 1, 1)]
        CF:EARNO||bigint||猪只耳号[:number(18, 1, 1)]
        CF:BREEDING||bigint||猪只品种[:number(18, 1, 1)]
        CF:BREEDING_NAME||string||猪只品种名称[:enum(esd2)]
        CF:PARITY||int||猪只胎次[:random_int(1,100)]
        CF:FARM_ID||bigint||猪只猪场ID[:number(18, 1, 1)]
        CF:MASTER_ORG_ID||bigint||猪只公司ID[:number(18, 1, 1)]
        CF:LANID||bigint||栏位ID[:number(18, 1, 1)]
        CF:LANNAME||string||栏位名称
        CF:SHEID||bigint||舍ID[:number(18, 1, 1)]
        CF:SHENAME||string||舍名称
        CF:LOUID||bigint||楼ID[:number(18, 1, 1)]
        CF:LOUNAME||string||楼名称
        CF:ESTATUS||string||猪只状态
        CF:PIGNUM||int||猪只当前带仔数[:random_int(1,100)]
    """
    test_tmpdir, meta_file = _make_tmp_file()

    cmd = 'datafaker hbase localhost:9090 pigtest 100 --meta {meta_file}'.format(meta_file=meta_file)

    _main(cmd, meta_content)


def test_hive():
    meta_content = """
        feed_date||string||饲喂日期（yyyy-mm-dd）[:date(-7d, -1d)]
        tenant_id||bigint||租户ID[:enum(162494980391305218)]
        farm_id||bigint||猪场ID[:enum(162498397843095552)]
        identity_id||string||猪只身份ID[:enum(LL05MLKS3G170201F40999)]
    """
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker hive hive://localhost:10000/yz_targetmetric_nuc dws_f_nuc_female_feeding_test 10 --meta {meta_file}'.format(meta_file=meta_file)
    _main(cmd, meta_content)


def test_op():
    meta_content = """
        id||int||自增id[:inc(id,1)]
        name||varchar(20)||学生名字[:name]
        nickname||varchar(20)||学生名字[:enum(xiao ming, hah, lele, esd f222)]
        age||int||学生年龄[:enum(3, 6, 7, 8, 9)]
        age2||int||学生年龄[:age(10, 20)]
        score||int||学生年龄[:inc(score, 10, 2)]
        allage||int||总年龄[:op(c0*c3+c4)]
        timestamp||varchar(20)||时间[:timestamp(1)]
        datetime||varchar(20)||时间[:datetime(1,%Y-%m-%d %H:%M)]
    """
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file . hello.txt 10 --meta {meta_file} --format text --outprint --format json'.format(meta_file=meta_file)
    _main(cmd, meta_content)


def test_es():
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker es localhost:9200 example1/tp1 100 --auth elastic:elastic --meta {meta_file} --format text'.format(meta_file=meta_file)
    _main(cmd)


def test_mysql():

    cmd = 'datafaker mysql mysql+mysqldb://root:root@localhost:3600/test pig_fnumbe_test 1 --meta data/meta.txt --format text'
    sys.argv = cmd.strip().split(' ')
    main()


def test_mysql_with_nometa():
    cmd = "datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10"
    sys.argv = cmd.strip().split(' ')
    main()


def test_int():
    meta_content = """
        id||int||not,
        name||varchar(200)||default,
        school||char(30)||default,
        nickname||char(30)||default,
        age||varchar(10)||default,
        class_num||char(10)||default,
        phone||int||default,
        email||char(10)||default,
        ip||char(10)||default,
        address||char(40)||default,
    """
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file . hello.txt 20 --meta {meta_file} --format text --outprint'.format(meta_file=meta_file)
    _main(cmd, meta_content)


def test_order_enum():
    meta_content = """
        id||int||not,
        nickname||varchar(20)||学生名字[:order_enum(xiao ming, hah, lele, esd, f222)]
        nickname2||varchar(20)||学生名字[:order_enum(xiao ming, hah, lele, esd, f222)]
        class_num||char(10)||default,
        phone||int||default,
        email||char(10)||default,
        ip||char(10)||default,
        address||char(40)||default,
    """
    test_tmpdir, meta_file = _make_tmp_file()
    cmd = 'datafaker file . hello.txt 21 --meta {meta_file} --format text --outprint'.format(meta_file=meta_file)
    _main(cmd, meta_content)
