#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from datafaker.cli import main

if __name__ == "__main__":

    #
    cmd = 'datagen mysql mysql+mysqldb://root:root@localhost:3600/test stu 10'
    # cmd = 'datagen kafka localhost:9092 hello 1 --meta /Users/lovelife/git/github/python/datagen/datagen/data/student.text --outprint'
    # cmd = 'datagen file out.txt hello 10 --meta /Users/lovelife/git/github/python/datagen/datagen/data/student.text --outprint --outfile output.txt'
    # cmd = 'datagen file out.txt hello 10 --meta /Users/lovelife/git/github/python/datagen/datagen/data/student.text --outfile output.txt'
    # cmd = 'datagen file out.txt hello 10 --meta /Users/lovelife/git/github/python/datagen/datagen/data/student.text'
    sys.argv = cmd.strip().split(' ')

    sys.exit(main())

