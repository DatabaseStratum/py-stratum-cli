from test.pgsql.DataLayer import DataLayer
from test.pgsql.StratumTestCase import StratumTestCase
import datetime


# ----------------------------------------------------------------------------------------------------------------------
class OverloadingTest(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_int(self):
        result = DataLayer.tst_test_argument_int(10)
        self.assertEqual(result, 10)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_big_int(self):
        result = DataLayer.tst_test_argument_big_int(15000)
        self.assertEqual(result, 15000)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_small_int(self):
        result = DataLayer.tst_test_argument_small_int(250)
        self.assertEqual(result, 250)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_bool(self):
        result = DataLayer.tst_test_argument_bool(True)
        self.assertEqual(result, True)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_numeric(self):
        result = DataLayer.tst_test_argument_numeric(15)
        self.assertEqual(result, 15)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_real(self):
        result = DataLayer.tst_test_argument_real(15.3)
        self.assertEqual(result, 15.3)

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_char(self):
        result = DataLayer.tst_test_argument_char("x")
        self.assertEqual(result, "x")

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_varchar(self):
        result = DataLayer.tst_test_argument_varchar("Really")
        self.assertEqual(result, "Really")

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_text(self):
        result = DataLayer.tst_test_argument_text("This is the test text")
        self.assertEqual(result, "This is the test text")

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_bit(self):
        result = DataLayer.tst_test_argument_bit(1)
        self.assertEqual(result, "0001")

        result = DataLayer.tst_test_argument_bit("110")
        self.assertEqual(result, "1100")

        result = DataLayer.tst_test_argument_bit("1010")
        self.assertEqual(result, "1010")

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_money(self):
        result = DataLayer.tst_test_argument_money('$12.34')
        self.assertEqual(result, '$12.34')

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_date(self):
        result = DataLayer.tst_test_argument_date("2015-01-01")
        self.assertEqual(result, datetime.date(2015, 1, 1))

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_bytea(self):
        result = DataLayer.tst_test_argument_bytea(b"This is the byte string")
        self.assertEqual(memoryview.tobytes(result), b"This is the byte string")

    # ------------------------------------------------------------------------------------------------------------------
    def test_argument_timestamp(self):
        result = DataLayer.tst_test_argument_timestamp("2015-01-01 12:00:00")
        self.assertEqual(result, datetime.datetime(2015, 1, 1, 12, 0))