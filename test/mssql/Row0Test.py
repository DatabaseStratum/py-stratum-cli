from test.mssql.DataLayerTestCase import DataLayerTestCase
from test.mssql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Row0Test(DataLayerTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type row0 must return null.
        """
        ret = DataLayer.tst_test_row0(0)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type row0 must return 1 row.
        """
        ret = DataLayer.tst_test_row0(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type row0 returns more than 1 rows.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            DataLayer.tst_test_row0(2)

# ----------------------------------------------------------------------------------------------------------------------
