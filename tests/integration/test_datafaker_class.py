#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys

from datafaker import main
from datafaker.cli import parse_args
from datafaker.testutils import FileCreator


class TestDataFaker:

    @classmethod
    def setup_class(cls):
        print('\nsetup_class()')

    @classmethod
    def teardown_class(cls):
        print('teardown_class()')

    def setup_method(self, method):
        self.test_tmpdir, self.meta_file = self._make_tmp_file()

    def teardown_method(self, method):
        print('\nteardown_method()')

    meta = """
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

    cmd = None
    def _main_file(self, cmd, meta=None):
        """
        以产生数据写到文件来集成测试
        :return:
        """

        if meta is None:
            meta = self.META_CONTENT

        sys.argv = cmd.strip().split(' ')
        args = parse_args()
        with open(args.meta, 'w') as fp:
            fp.write(meta)

        main()
        outfile = os.path.join(args.connect, args.table)
        with open(outfile) as fp:
            result = fp.read().splitlines()
        return result

    def _main(self, cmd):

        sys.argv = cmd.strip().split(' ')
        args = parse_args()
        with open(args.meta, 'w') as fp:
            fp.write(self.meta)
        main()


    def _make_tmp_file(self):
        fc = FileCreator()
        test_tmpdir = fc.create_dir("testdata")
        meta_file = os.path.join(test_tmpdir, "schema.txt")
        return test_tmpdir, meta_file

    def test_cmd(self):
        test_tmpdir, meta_file = self._make_tmp_file()
        sys.argv = self.cmd.strip().split(' ')
        args = parse_args()
        with open(args.meta, 'w') as fp:
            fp.write(self.meta)

        result = self._main_file(self.cmd)


    def test_fake_data_to_file(self):

        cmd = 'datafaker file {connect} hello.txt 10 --meta {meta_file}'.format(connect=self.test_tmpdir, meta_file=self.meta_file)
        result = self._main_file(cmd)
        assert 10 == len(result)

