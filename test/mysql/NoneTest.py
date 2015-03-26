from test.mysql.DataLayerTestCase import DataLayerTestCase
from test.mysql.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class NoneTest(DataLayerTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type none must return the number of rows affected.
        """
        ret = DataLayer.tst_test_none(0)
        self.assertEqual(0, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type none must return the number of rows affected.
        """
        ret = DataLayer.tst_test_none(1)
        self.assertEqual(1, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        Stored routine with designation type none must return the number of rows affected.
        """
        ret = DataLayer.tst_test_none(20)
        self.assertEqual(20, ret)

# ----------------------------------------------------------------------------------------------------------------------
