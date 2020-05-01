#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

"""
对正则表达式函数的封装

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""
import re


def reg_keyword(data):
    """
    从表字段里面提取出关键词，格式为：
    ***[:###]***
    提取出###
    :param data:
    :return:
    """
    patt = re.compile(r".*\[:(.+)\].*")
    ret = patt.findall(data)
    return ret[0] if ret else None


def reg_all_keywords(data):
    """
    从meta file中提取所有关键词，格式为：
    ***[:###]***
    提取出###
    :param data:
    :return:
    """
    patt = re.compile(r"\[:([^\[\]]+)\]")
    ret = patt.findall(data)
    return ret if ret else None


def reg_replace_keywords(data, repl="%s"):

    ret = re.sub(r"(\[:[^\[\]]+\])", repl, data)
    return ret


def reg_args(data):
    # patt = re.compile(r"(?<=[\(|,\s*])\w+")
    # ret = patt.findall(data)
    if '(' not in data:
        return []
    ret = data[data.find('(')+1: data.find(')')]
    return [arg.strip() for arg in ret.split(',')]


def reg_cmd(data):
    """
    提取keyword中具体命令,格式为:
    [:cmd()] 或者 [:cmd]
    :param data: [:cmd()] 或者 [:cmd]
    :return: cmd
    """
    patt = re.compile(r"(.+)\(.*")
    ret = patt.findall(data)
    return ret[0] if ret else data


def reg_float(data):
    """
    匹配浮点型数字
    :param data: 
    :return: 
    """
    patt = re.compile(r"(\d+[\.\d]\d+)")
    ret = patt.findall(data)
    return float(ret[0]) if ret else 0


def reg_integer(data):
    patt = re.compile(r"(\d+)")
    return patt.findall(data)


def reg_int(data):
    """
    匹配整数
    :param data: 
    :return: 
    """

    ret = reg_integer(data)
    return int(ret[0]) if ret else 0


def reg_all_int(data):
    """
    匹配所有整数
    :param data: 
    :return: 整数list
    """
    patt = re.compile(r"(\d+)")
    ret = patt.findall(data)
    return [int(dd) for dd in ret]


def reg_int_first(data):
    """
    匹配字符串中第一个数字串
    :param data: 
    :return: 
    """
    nums = reg_all_int(data)
    return nums[0] if nums else None


def reg_date(data):
    """匹配日期"""
    patt = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})")
    ret = patt.findall(data)

    if not ret:
        patt = re.compile(r"(\d{4}年\d{1,2}月\d{1,2}日)")
        ret = patt.findall(data)
    return ret[0] if ret else ''


def reg_start(data, start):
    """
    匹配以start字符串开头的，空格分隔的下一个字符串
    :param data: 
    :param start: 
    :return: 
    """
    patt = re.compile(r".*%s[\s]*(\S+)[\s]*.*" % (start,))
    ret = patt.findall(data)
    return ret[0] if ret else ''


def reg_all_chinese(data):
    """
    匹配所有的汉字
    :param data: 
    :return: 汉字list
    """
    patt = re.compile(u'[\u4e00-\u9fa5]+?')
    ret = patt.findall(data)
    return ret


def reg_match(reg_str, targetstr):
    """
    正则match函数匹配
    :param reg_str: 规则字符串
    :param targetstr:  目标字符串
    :return:
    """
    m = re.match(reg_str, targetstr)
    return m


def reg_search(reg_str, targetstr):
    """
    正则search函数匹配
    :param reg_str: 规则字符串
    :param targetstr:  目标字符串
    :return:
    """
    m = re.search(reg_str, targetstr)
    return m



