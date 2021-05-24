#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to test info_file functions
"""
# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
# from future.builtins import *  # NOQA @UnusedWildImport

import os
from pathlib import Path
import unittest
import inspect

from campaigninfo.info_files.yamlref import load as yamlref_load


class TestADDONSMethods(unittest.TestCase):
    """
    Test suite for misc obsinfo operations.
    """
    def setUp(self):
        self.path = Path("").resolve().parent
        self.testing_path = self.path / "tests" / "data"
        self.example_files_path = self.path / '_examples'

    def test_yamlref_load(self):
        """
        Test yamlref reading of identical json and yaml files
        """
        with open(self.testing_path / 'test_noref.yaml') as fp:
            a = yamlref_load(fp)
        with open(self.testing_path / 'test_noref.json') as fp:
            b = yamlref_load(fp)
        self.assertTrue(a == b)


def suite():
    return unittest.makeSuite(TestADDONSMethods, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
