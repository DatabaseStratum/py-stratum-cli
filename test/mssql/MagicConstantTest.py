import os
from test.mssql.DataLayer import DataLayer
from test.mssql.StratumTestCase import StratumTestCase


# ----------------------------------------------------------------------------------------------------------------------
class MagicConstantTest(StratumTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Test constant __ROUTINE__. Must return name of routine.
        """
        ret = DataLayer.dbo_tst_magic_constant01()
        self.assertEqual('dbo.tst_magic_constant01', ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Test constant __LINE__. Must return line number in the source code.
        """
        ret = DataLayer.dbo_tst_magic_constant02()
        self.assertEqual(4, int(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        Test constant __FILE__. Must return the filename of the source of the routine.
        """
        dir_cur_file = os.path.dirname(os.path.abspath(__file__))
        path = os.path.realpath(dir_cur_file + "/psql/dbo.tst_magic_constant03.psql")
        filename = os.path.realpath(path)
        ret = DataLayer.dbo_tst_magic_constant03()
        self.assertEqual(filename, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test4(self):
        """
        Test constant __DIR__. Must return name of the folder where the source file of routine the is located.
        """
        dir_cur_file = os.path.dirname(os.path.abspath(__file__))
        dir_name = os.path.realpath(dir_cur_file + '/psql')
        ret = DataLayer.dbo_tst_magic_constant04()
        self.assertEqual(dir_name, ret)

# ----------------------------------------------------------------------------------------------------------------------
