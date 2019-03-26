#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kafka import KafkaProducer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def load_sqlalchemy(connet):
    """
    返回db session
    :param connet:
    :return:
    """
    engine = create_engine(connet, pool_recycle=1800)
    DBSession = sessionmaker(engine)
    session = DBSession()
    return session


def load_kafka(brokers):
    producer = KafkaProducer(bootstrap_servers=brokers)
    return producer