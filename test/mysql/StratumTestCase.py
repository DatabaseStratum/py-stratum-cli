import sys
import unittest
from io import StringIO
from test.mysql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class StratumTestCase(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        DataLayer.config['host'] = 'localhost'
        DataLayer.config['user'] = 'test'
        DataLayer.config['password'] = 'test'
        DataLayer.config['database'] = 'test'

        DataLayer.connect()

        self.held, sys.stdout = sys.stdout, StringIO()

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        sys.stdout = self.held
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------
