from test.mssql.StratumTestCase import StratumTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Singleton1Test(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type singleton1 must return 1 value and 1 value only.
        """
        ret = DataLayer.dbo_tst_test_singleton1(1)
        self.assertEqual(1, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        An exception must be thrown when a stored routine with designation type singleton1 returns 0 values.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            DataLayer.dbo_tst_test_singleton1(0)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type singleton1 returns more than 1 values.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            DataLayer.dbo_tst_test_singleton1(2)

# ----------------------------------------------------------------------------------------------------------------------
