#!/usr/bin/env python
# -*- coding: UTF-8 -*-



import sqlparse

import re

def test_sqlparse():
    sql = """
    create table TEST_MODULE;
    create table TEST_MODULE
    (
      MODULE_ID            NUMBER NOT NULL,
      MODULE_NAME          VARCHAR2(64) NOT NULL,
      USER_ID              VARCHAR2(32) NOT NULL, -----这是;注释---;u'哈哈'asd;fasfda
      MODULE_TYPE          VARCHAR2(16) DEFAULT '1', --hello
      PARENT_MODULE_ID     NUMBER DEFAULT 1,
      SORT                 NUMBER(10) DEFAULT 1,
      CREATED_BY           VARCHAR2(64),
      CREATED_DATE         DATE DEFAULT SYSDATE,
      UPDATED_BY           VARCHAR2(64),
      UPDATED_DATE         DATE--reret
    );
    ---adfdokfd
    drop table TEST_MODULE;
    drop table TEST_MODULE; --strsfsdff
    create table TEST_MODULE
    (
      MODULE_ID            NUMBER NOT NULL,
      MODULE_NAME          VARCHAR2(64) NOT NULL,
      USER_ID              VARCHAR2(32) NOT NULL, -----这是;注释---;u'哈哈'asd;fasfda
      MODULE_TYPE          VARCHAR2(16) DEFAULT '1', --hello
      PARENT_MODULE_ID     NUMBER DEFAULT 1,
      SORT                 NUMBER(10) DEFAULT 1,
      CREATED_BY           VARCHAR2(64),
      CREATED_DATE         DATE DEFAULT SYSDATE,
      UPDATED_BY           VARCHAR2(64),
      UPDATED_DATE         DATE--reret
    );
    create table TEST_MODULE;
    """
    for item in sqlparse.split(sql):
        print
        item, '@@@@@@@@@@@@'

    uncomment_list = """
    create table TEST_MODULE;
    create table TEST_MODULE
    (
      MODULE_ID            NUMBER NOT NULL,
      MODULE_NAME          VARCHAR2(64) NOT NULL,
      USER_ID              VARCHAR2(32) NOT NULL, -----这是;注释---;u'哈哈'asd;fasfda
      MODULE_TYPE          VARCHAR2(16) DEFAULT '1', --hello
      PARENT_MODULE_ID     NUMBER DEFAULT 1,
      SORT                 NUMBER(10) DEFAULT 1,
      CREATED_BY           VARCHAR2(64),
      CREATED_DATE         DATE DEFAULT SYSDATE,
      UPDATED_BY           VARCHAR2(64),
      UPDATED_DATE         DATE--reret
    );
    ---adfdokfd
    drop table TEST_MODULE;
    drop table TEST_MODULE; 
    create table TEST_MODULE
    (
      MODULE_ID            NUMBER NOT NULL,
      MODULE_NAME          VARCHAR2(64) NOT NULL,
      USER_ID              VARCHAR2(32) );NOT NULL, -----这是;注释---;u'哈哈'asd;fasfda
      MODULE_TYPE          VARCHAR2(16) DEFAULT '1', --hello
      PARENT_MODULE_ID     NUMBER DEFAULT 1,
      SORT                 NUMBER(10) DEFAULT 1,
      CREATED_BY           VARCHAR2(64),
      CREATED_DATE         DATE DEFAULT SYSDATE,
      UPDATED_BY           VARCHAR2(64),
      UPDATED_DATE         DATE--reret
    );
    create table TEST_MODULE;
    """


    def trans_sql(sql_strs):
        sql_strs = sql_strs.replace("\r\n", "\n").replace("\r", "\n")
        sql_list = sql_strs.split('\n')

        sql_sts_list = []

        for item in sql_list:
            if len(item) == 0:
                continue
            if item.strip().startswith("--"):
                continue
            if re.search(r';\s*$', item) and not re.search(r'\)\s*;$', item):
                sql_sts_list.append(item)
            else:

                if len(sql_sts_list) == 0:
                    sql_sts_list.append(item + "\n")
                elif sql_sts_list[len(sql_sts_list) - 1].endswith(";"):
                    sql_sts_list.append(item + "\n")
                else:
                    sql_sts_list[len(sql_sts_list) - 1] += (item + "\n")
        for index, item in enumerate(sql_sts_list):
            if re.search(r';\s*$', item):
                sql_sts_list[index] = re.sub(r';\s*$', "", item)
            if re.search(r'\)\s*;\n$', item):
                sql_sts_list[index] = re.sub(r'\)\s*;\n$', ")", item)
        return sql_sts_list


    sql_list = trans_sql(uncomment_list)

    for item in sql_list:
        print
        item, '################'



    # !/usr/bin/env python
    # -*- coding: utf-8 -*-

    import multiprocessing

    uncomment_list = """
    drop table TEST_MODULE;
    create table TEST_MODULE
    (
      MODULE_ID            NUMBER NOT NULL,
      MODULE_NAME          VARCHAR2(64) NOT NULL,
      USER_ID              VARCHAR2(32) NOT NULL, -----这是;注释---;哈哈asd;fasfda
      MODULE_TYPE          VARCHAR2(16) DEFAULT '1', --hello
      PARENT_MODULE_ID     NUMBER DEFAULT 1,
      SORT                 NUMBER(10) DEFAULT 1,
      CREATED_BY           VARCHAR2(64),
      CREATED_DATE         DATE DEFAULT SYSDATE,
      UPDATED_BY           VARCHAR2(64),
      UPDATED_DATE         DATE--reret
    );
    drop table TEST_MODULE;
    """
    temp_content_item1 = uncomment_list.replace("\r\n", "\n")
    temp_content_item2 = temp_content_item1.replace("\r", "\n")
    uncomment_list = temp_content_item2.split('\n')

    sql_sts_list = []
    for_int = 0
    for index, item in enumerate(uncomment_list):

        if len(item) == 0:
            continue
        if item.strip().endswith(";"):
            item = item[:-1]
            sql_sts_list.append(item)
        else:
            print
            len(sql_sts_list)
            sql_sts_list.append(item)
        # print
        # sql_sts_list

    print(sql_sts_list)