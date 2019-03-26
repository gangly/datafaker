#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import sys
import traceback

from datafaker.constant import __version__

def parse_args():

    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='Generates SQLAlchemy model code from an existing database.')
    parser.add_argument('dbtype', nargs='?', action='store', help='data source type')
    parser.add_argument('connect', nargs='?', action='store', help='connect info to the database')
    parser.add_argument('table', action='store', help='table to process')
    parser.add_argument('num', nargs='?', action='store', type=int, help='number of records to generate')
    parser.add_argument('--meta', nargs='?', action='store', help='meta file path')
    parser.add_argument('--interval', action='store', type=int, default=1, help='meta file path')
    parser.add_argument('--version', action='store_true', help="print the version number and exit")
    parser.add_argument('--outprint', action='store_true', help="print fake date to screen")
    parser.add_argument('--outspliter', action='store', help="print data, to split columns")
    parser.add_argument('--locale', action='store', default='zh_CN', help='which country language')
    parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    parser.add_argument('--format', default='text', help='outprint and outfile format: json, text (default: text)')
    args = parser.parse_args()

    if not args.dbtype:
        print('You must supply a dbtype\n')
        parser.print_help()
        exit(0)

    if not args.connect:
        print('You must supply a connect\n')
        parser.print_help()
        exit(0)

    # args.connect = "mysql+mysqldb://root:root@localhost:3600/test"
    # args.table = 'stu'
    # url = "hive://yarn@hdfs03-dev.yingzi.com:10000/default?auth=NONE"
    # table = 'ads_brc_rpt_all_entry_month'
    # args.num = 100
    # args.dbtype = 'mysql'
    # args.outprint = True
    # args.outfile = 'out.txt'
    # args.meta = '/Users/lovelife/git/github/python/datagen/datagen/data/student.text'

    return args


def load_db_class(dbtype):
    """
    read subcommand from subcmds directory
    :return: subcommands list
    """
    pkgname = 'datafaker.dbs.' + dbtype + 'db'
    classname = dbtype.capitalize() + 'DB'
    module = __import__(pkgname, fromlist=(classname))
    db_class = getattr(module, classname)
    return db_class


def main():

    try:
        args = parse_args()
        db = load_db_class(args.dbtype)(args)
        db.do_fake()
    except Exception as e:
        msg = traceback.format_exc()
        print(msg)
        print(e)