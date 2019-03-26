#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from drivers import load_sqlalchemy

url = "mysql+mysqldb://root:root@localhost:3600/test"

def test_metadata():

    tables = ['stu', ]
    schema = None
    noviews = True
    engine = create_engine(url)
    metadata = MetaData(engine)
    # tables = tables if tables else None
    metadata.reflect(engine, schema, not noviews, tables)
    print(metadata.tables['stu'].columns['age'].type)
    print()



def test_excute():
    session = load_sqlalchemy(url)

    sql = "show full columns from stu"
    rows = session.execute(sql)

    for row in rows:
        print(row)
