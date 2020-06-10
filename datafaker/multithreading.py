#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ctypes
import threading


class StoppableThread(threading.Thread):
    """Thread class with a terminate() method. The thread itself has to check
    regularly for the stopped() condition."""

    def terminate(self):
        self._stop_event = threading.Event()
        self._stop_event.set()
        raise KeyboardInterrupt

    def stopped(self):
        return self._stop_event.is_set()


# Process = threading.Thread
Process = StoppableThread
Lock = threading.Lock
typecode_to_type = {
    'c': ctypes.c_char, 'u': ctypes.c_wchar,
    'b': ctypes.c_byte, 'B': ctypes.c_ubyte,
    'h': ctypes.c_short, 'H': ctypes.c_ushort,
    'i': ctypes.c_int, 'I': ctypes.c_uint,
    'l': ctypes.c_long, 'L': ctypes.c_ulong,
    'f': ctypes.c_float, 'd': ctypes.c_double
}


class Value(object):
    def __init__(self, typecode, value):
        self.value = typecode_to_type.get(typecode)(value).value


List = list
Dict = dict

