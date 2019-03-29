#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import unittest

import mock

from datafaker.testutils import FileCreator


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





