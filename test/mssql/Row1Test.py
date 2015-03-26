from test.mssql.DataLayerTestCase import DataLayerTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Row1Test(DataLayerTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type row1 must return 1 row and 1 row only.
        """
        ret = DataLayer.tst_test_row1(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns 0 rows.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            DataLayer.tst_test_row1(0)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns more than 1 rows.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            DataLayer.tst_test_row1(2)

# ----------------------------------------------------------------------------------------------------------------------
