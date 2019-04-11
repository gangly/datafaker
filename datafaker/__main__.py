#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from datafaker.cli import main

if __name__ == "__main__":

    #
    # cmd = 'datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10'
    # # cmd = 'datafaker kafka localhost:9092 hello 1 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outprint'
    # # cmd = 'datafaker file out.txt hello 10 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outprint --outfile output.txt'
    # # cmd = 'datafaker file out.txt hello 10 --meta /Users/lovelife/git/github/python/datafaker/datafaker/data/student.text --outfile output.txt'
    # cmd = 'datafaker file out.txt hello 10 --meta data/student.text'
    # cmd = 'datafaker file . hello.txt 10 --meta data/student.text --outprint --outspliter ## --withheader'
    # cmd = 'datafaker hive hive://yarn@hdfs03-dev.yingzi.com:10000/default acidtest_nocluster 10'
    # cmd = 'datafaker hbase localhost:9090 pigtest 2 --meta data/hbase.txt'
    # sys.argv = cmd.strip().split(' ')

    sys.exit(main())

