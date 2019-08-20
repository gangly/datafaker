#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from __future__ import unicode_literals


class BaseError(Exception):
    """
    The base exception class for datafaker base exceptions.

    :ivar msg: The descriptive message associated with the error.
    """
    fmt = 'An unspecified error occurred'

    def __init__(self, fmt=None, **kwargs):
        if fmt is not None:
            self.fmt = fmt
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class ConfigParseError(BaseError):
    """
    config file error
    """
    fmt = 'Parse config file error.'


class FileNotFoundError(BaseError):
    """
    file not found
    """
    def __init__(self, filepath=''):
        Exception.__init__(self, "error, %s not found!" % filepath)


class MetaFileError(BaseError):
    """
    file not found
    """
    fmt = 'meta file not found, please set meta parameter.'


class EnumMustNotEmptyError(BaseError):
    """
    file not found
    """
    fmt = 'enum type must not be empty'


class ParseSchemaError(BaseError):
    fmt = 'parse schema error.'


class ParamValidationError(BaseError):
    fmt = 'Parameter validation failed:\n{report}'


class ParamError(BaseError):
    fmt = 'parameter error'
