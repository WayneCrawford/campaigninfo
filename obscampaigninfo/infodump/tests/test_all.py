#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to test obsinfo/misc functions
"""
from pathlib import Path
import unittest
import filecmp

from obscampaigninfo.infodump import infodump


class TestADDONSMethods(unittest.TestCase):
    """
    Test suite for misc obsinfo operations.
    """
    def setUp(self):
        self.path = Path("").resolve().parent
        self.testing_path = self.path / "tests" / "data"
        self.examples_path = self.path.parent / "_examples"

    def test_infodump(self):
        """
        Compare output with an example file
        """
        for in_file in self.examples_path.glob("MOMAR*_A.campaign.yaml"):
            out_fname = infodump(str(in_file), quiet=True)
            self.assertTrue(filecmp.cmp(out_fname,
                                        self.testing_path / out_fname,
                                        shallow=False))
            Path(out_fname).unlink()


def suite():
    return unittest.makeSuite(TestADDONSMethods, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
