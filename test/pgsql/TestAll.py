import unittest
from test.pgsql.StratumTestCase import StratumTestCase
from test.pgsql.FunctionTest import FunctionTest
from test.pgsql.LogTest import LogTest
from test.pgsql.MagicConstantTest import MagicConstantTest
from test.pgsql.Row0Test import Row0Test
from test.pgsql.Row1Test import Row1Test
from test.pgsql.RowsTest import RowsTest
from test.pgsql.RowsWithIndexTest import RowsWithIndexTest
from test.pgsql.RowsWithKeyTest import RowsWithKeyTest
from test.pgsql.Singleton0Test import Singleton0Test
from test.pgsql.Singleton1Test import Singleton1Test


# ----------------------------------------------------------------------------------------------------------------------
class TestAll(StratumTestCase):

    def test(self):
        suite = unittest.TestSuite()
        suite.addTest(FunctionTest())
        suite.addTest(LogTest())
        suite.addTest(MagicConstantTest())
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
