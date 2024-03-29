#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to test obsinfo/misc functions
"""
# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
# from future.builtins import *  # NOQA @UnusedWildImport

import os
from pathlib import Path
import unittest
import inspect

from obscampaigninfo.experiment_to_campaigns import _experiment_to_campaigns
from obscampaigninfo.info_files import validate, _read_json_yaml


class TestADDONSMethods(unittest.TestCase):
    """
    Test suite for misc obsinfo operations.
    """
    def setUp(self):
        self.path = Path("").resolve().parent
        self.testing_path = self.path / "tests" / "data"
        # self.path = os.path.dirname(os.path.abspath(inspect.getfile(
        #     inspect.currentframe())))
        # self.testing_path = os.path.join(self.path, "data")
        self.example_files_path = self.path / '_examples'

    def test_validate(self):
        """
        Test validate files
        """
        for fname in self.example_files_path.glob("*.yaml"):
            self.assertTrue(validate(str(fname), quiet=True))

    def test_experiment_to_campaigns(self):
        """
        Test creation of campaign files from experiment file
        """
        _experiment_to_campaigns(
            str(self.example_files_path / "MOMAR.experiment.yaml"), quiet=True)
        for test_file in (self.testing_path / "yamls_out").glob("MOMAR*.campaign.yaml"):
            a = _read_json_yaml(str(test_file))
            b = _read_json_yaml(test_file.name)
            self.assertDictEqual(a, b)
            # print(test_file)
            Path(test_file.name).unlink()


def suite():
    return unittest.makeSuite(TestADDONSMethods, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
