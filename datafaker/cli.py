#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import sys
import traceback


from datafaker.constant import __version__, DEFAULT_INTERVAL, DEFAULT_FORMAT, DEFAULT_LOCALE, BATCH_SIZE, WORKERS


def parse_args():

    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='datafaker, a tool to make generate data easy.')
    parser.add_argument('dbtype', nargs='?', action='store', help='data source type')
    parser.add_argument('connect', nargs='?', action='store', help='connect info to the database')
    parser.add_argument('table', action='store', help='table to process')
    parser.add_argument('num', nargs='?', action='store', type=int, help='number of records to generate')
    parser.add_argument('--auth', nargs='?', action='store', help='user and password')
    parser.add_argument('--meta', nargs='?', action='store', help='meta file path')
    parser.add_argument('--interval', action='store', type=float, help='the interval to make stream data')
    parser.add_argument('--batch', action='store', type=int, default=BATCH_SIZE, help='the interval to make stream data')
    parser.add_argument('--workers', action='store', type=int, default=WORKERS, help='the interval to make stream data')
    parser.add_argument('--version', action='store_true', help="print the version number and exit")
    parser.add_argument('--outprint', action='store_true', help="print fake date to screen")
    parser.add_argument('--outspliter', action='store', help="print data, to split columns")
    parser.add_argument('--locale', action='store', default=DEFAULT_LOCALE, help='locale language')
    parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    parser.add_argument('--format', default=DEFAULT_FORMAT, help='outprint and outfile format: json, text (default: text)')
    parser.add_argument('--withheader', action='store_true', help='print data or write data to file with column header')
    args = parser.parse_args()

    if not args.dbtype:
        print('You must supply a dbtype\n')
        parser.print_help()
        exit(0)

    if not args.connect:
        print('You must supply a connect\n')
        parser.print_help()
        exit(0)

    if not args.table:
        print('You must supply a table\n')
        parser.print_help()
        exit(0)

    if not args.num:
        print('You must supply number of records\n')
        parser.print_help()
        exit(0)

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
