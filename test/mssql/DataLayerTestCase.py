from io import StringIO
import unittest
import sys
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayerTestCase(unittest.TestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        DataLayer.connect('192.168.137.7', 'test', 'test', 'test')
        #self.held, sys.stdout = sys.stdout, StringIO()

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        #sys.stdout = self.held
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------
