import unittest
from test.mysql.StratumTestCase import StratumTestCase
from test.mysql.FunctionTest import FunctionTest
from test.mysql.LogTest import LogTest
from test.mysql.MagicConstantTest import MagicConstantTest
from test.mysql.NoneTest import NoneTest
from test.mysql.Row0Test import Row0Test
from test.mysql.Row1Test import Row1Test
from test.mysql.RowsTest import RowsTest
from test.mysql.RowsWithIndexTest import RowsWithIndexTest
from test.mysql.RowsWithKeyTest import RowsWithKeyTest
from test.mysql.Singleton0Test import Singleton0Test
from test.mysql.Singleton1Test import Singleton1Test


# ----------------------------------------------------------------------------------------------------------------------
class TestAll(StratumTestCase):

    def test(self):
        suite = unittest.TestSuite()
        suite.addTest(FunctionTest())
        suite.addTest(LogTest())
        suite.addTest(MagicConstantTest())
        suite.addTest(NoneTest())
        suite.addTest(Row0Test())
        suite.addTest(Row1Test())
        suite.addTest(RowsTest())
        suite.addTest(RowsWithIndexTest())
        suite.addTest(RowsWithKeyTest())
        suite.addTest(Singleton0Test())
        suite.addTest(Singleton1Test())
        #suite.addTest(TableTest())
        return suite

# ----------------------------------------------------------------------------------------------------------------------
