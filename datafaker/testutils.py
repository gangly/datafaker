#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import random
import shutil
import string
import tempfile

from datafaker.exceptions import ParamValidationError


def random_string(size):
    return ''.join(random.sample(string.ascii_letters + string.digits, size))


POSTFIXES = ('B', 'K', 'M', 'G', 'T', 'P', 'E')


def bytes_to_unitstr(bytes):
    """
    transform 1024 to 1.0k
    2.3*1024*1024 to 2.3M
    :param bytes:
    :return:
    """
    base = 1024
    format = '%.1f%s'
    for i, postfix in enumerate(POSTFIXES):
        unit = base ** (i+1)
        if round((1.0 * bytes / unit) * base) < base:
            value = 1.0*bytes / (base**i)
            if i == 0:
                format = '%d%s'

            return format % (value, postfix)

POSTFIXES = ('B', 'K', 'M', 'G', 'T', 'P', 'E')

def unitstr_to_bytes(unitstr):
    """
    transform 1M to 1024*1024
    1.2K to int(1.2*1024)
    :param unitstr:
    :return:
    """
    digit = unitstr[:-1]
    unit = unitstr[-1].upper()
    if unit.isdigit():
        return int(float(unitstr)) if '.' in unitstr else int(unitstr)
    if unit not in POSTFIXES:
        raise ParamValidationError(**{'report': '%s unit must be in %s' % (unitstr, POSTFIXES)})

    base = 1024
    return int(float(digit) * base ** POSTFIXES.index(unit))


class FileCreator(object):
    def __init__(self):
        self.rootdir = tempfile.mkdtemp()

    def remove_all(self, path=None):
        if path:
            shutil.rmtree(path)
        shutil.rmtree(self.rootdir)

    def create_full_dir(self, rootdir, dirname, filenum=0, names=None, sizelist=None):
        tmpdir = self.rootdir
        self.rootdir = rootdir
        fullpath = self.create_dir(dirname, filenum, names, sizelist)
        self.rootdir = tmpdir
        return fullpath

    def create_dir(self, dirname, filenum=0, names=None, sizelist=None):
        tmpdir = self.rootdir
        self.rootdir = os.path.join(self.rootdir, dirname)

        os.mkdir(self.rootdir)
        for i in range(filenum):
            name = names[i] if names and i < len(names) else random_string(8)
            size = sizelist[i] if sizelist and i < len(sizelist) else '8B'
            self.create_size_file(name, size)
        fulldir = self.rootdir
        self.rootdir = tmpdir
        return fulldir

    def create_size_file(self, filename, size):
        size = unitstr_to_bytes(size)
        full_path = os.path.join(self.rootdir, filename)
        with open(full_path, 'w') as fp:
            fp.seek(size-1)
            fp.write('a')
            fp.close()
        return full_path

    def create_file(self, filename, contents=None, mtime=None, mode='w'):
        """Creates a file in a tmpdir

        ``filename`` should be a relative path, e.g. "foo/bar/baz.txt"
        It will be translated into a full path in a tmp dir.

        If the ``mtime`` argument is provided, then the file's
        mtime will be set to the provided value (must be an epoch time).
        Otherwise the mtime is left untouched.

        ``mode`` is the mode the file should be opened either as ``w`` or
        `wb``.

        Returns the full path to the file.

        """
        contents = contents if contents else random_string(8)
        full_path = os.path.join(self.rootdir, filename)
        if not os.path.isdir(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, mode) as f:
            f.write(contents)
        current_time = os.path.getmtime(full_path)
        # Subtract a few years off the last modification date.
        os.utime(full_path, (current_time, current_time - 100000000))
        if mtime is not None:
            os.utime(full_path, (mtime, mtime))
        return full_path

    def append_file(self, filename, contents):
        """Append contents to a file

        ``filename`` should be a relative path, e.g. "foo/bar/baz.txt"
        It will be translated into a full path in a tmp dir.

        Returns the full path to the file.
        """
        full_path = os.path.join(self.rootdir, filename)
        if not os.path.isdir(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, 'a') as f:
            f.write(contents)
        return full_path

    def full_path(self, filename):
        """Translate relative path to full path in temp dir.

        f.full_path('foo/bar.txt') -> /tmp/asdfasd/foo/bar.txt
        """
        return os.path.join(self.rootdir, filename)



