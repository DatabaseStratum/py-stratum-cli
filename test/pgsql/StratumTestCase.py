"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import sys
import unittest
from io import StringIO

from test.pgsql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class StratumTestCase(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        DataLayer.connect('localhost', 'test', 'test', 'test', 'test')

        self.held, sys.stdout = sys.stdout, StringIO()

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        sys.stdout = self.held
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------
