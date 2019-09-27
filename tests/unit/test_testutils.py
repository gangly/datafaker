#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import unittest

from datafaker.testutils import FileCreator
from datafaker.utils import read_file_lines

class TestFileCreator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fc = FileCreator()

    @classmethod
    def tearDownClass(cls):
        cls.fc.remove_all()

    def test_create_file(self):
        fullpath = self.fc.create_file('file')
        self.assertEqual(os.path.exists(fullpath), True)
        self.assertEqual(os.path.getsize(fullpath), 8)

    def test_create_size_file(self):
        fullpath = self.fc.create_size_file('file.txt', '8K')
        self.assertEqual(os.path.getsize(fullpath), 8*1024)

    def test_read_file_lines(self):
        filepath = "__init__.py"
        read_file_lines(filepath)





