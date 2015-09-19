import sys
import unittest
from io import StringIO

from test.pgsql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class StratumTestCase(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        DataLayer.connect('localhost', 'cbi', 'test', 'test', 'test')

        self.held, sys.stdout = sys.stdout, StringIO()

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        sys.stdout = self.held
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------
