"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import sys

from test.DataLayer import DataLayer
from test.StratumTestCase import StratumTestCase


class LogTest(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type none must return the number of rows affected.
        """
        n = DataLayer.tst_test_log()

        self.assertEqual(2, n)

        self.assertRegex(sys.stdout.getvalue(),
                         '^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\sHello, world\n){2}$')

# ----------------------------------------------------------------------------------------------------------------------
