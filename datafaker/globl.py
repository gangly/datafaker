#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from hcmd import compat


def init():
    global _global_dict
    _global_dict = {}


def use_lock(key):
    lock_key = key + '_lock'
    if lock_key not in _global_dict:
        _global_dict[lock_key] = compat.Lock()
    return lock_key


def set_value(key, value):
    _global_dict[key] = value


def set_value_lock(key, value):
    lock_key = use_lock(key)
    with _global_dict[lock_key]:
        _global_dict[key].value = value


def get_value(key, default=None):
    try:
        return _global_dict[key]
    except KeyError:
        return default


def append_list_lock(key, value):
    lock_key = use_lock(key)
    with _global_dict[lock_key]:
        _global_dict[key].append(value)

def exists(key):
    return key in _global_dict