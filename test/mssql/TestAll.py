import unittest
from test.mssql.StratumTestCase import StratumTestCase
from test.mssql.MagicConstantTest import MagicConstantTest
from test.mssql.FunctionTest import FunctionTest
from test.mssql.Row0Test import Row0Test
from test.mssql.Row1Test import Row1Test
from test.mssql.RowsTest import RowsTest
from test.mssql.RowsWithIndexTest import RowsWithIndexTest
from test.mssql.RowsWithKeyTest import RowsWithKeyTest
from test.mssql.Singleton0Test import Singleton0Test
from test.mssql.Singleton1Test import Singleton1Test


# ----------------------------------------------------------------------------------------------------------------------
class TestAll(StratumTestCase):

    def test(self):
        suite = unittest.TestSuite()
        suite.addTest(MagicConstantTest())
        suite.addTest(FunctionTest())
        suite.addTest(Row0Test())
        suite.addTest(Row1Test())
        suite.addTest(RowsTest())
        suite.addTest(RowsWithIndexTest())
        suite.addTest(RowsWithKeyTest())
        suite.addTest(Singleton0Test())
        suite.addTest(Singleton1Test())
        return suite

# ----------------------------------------------------------------------------------------------------------------------
