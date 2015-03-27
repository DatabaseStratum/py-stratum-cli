from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer(StaticDataLayer):

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant01():
        return StaticDataLayer.execute_singleton1('exec dbo.tst_magic_constant01')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant02():
        return StaticDataLayer.execute_singleton1('exec dbo.tst_magic_constant02')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant03():
        return StaticDataLayer.execute_singleton1('exec dbo.tst_magic_constant03')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant04():
        return StaticDataLayer.execute_singleton1('exec dbo.tst_magic_constant04')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0(p_count):
        return StaticDataLayer.execute_row0('exec dbo.tst_test_row0 %s' % p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1(p_count):
        return StaticDataLayer.execute_row1('exec dbo.tst_test_row1 %s' % p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows(p_count):
        return StaticDataLayer.execute_rows('exec dbo.tst_test_rows %s' % p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1(p_count):
        rows = StaticDataLayer.execute_rows('exec dbo.tst_test_rows_with_index1 %s' % p_count)
        if rows:
            return {rows[0]['tst_c01']: {rows[0]['tst_c02']: rows}}
        else:
            return {}

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_key1(p_count):
        ret = {}
        rows = StaticDataLayer.execute_rows('exec dbo.tst_test_rows_with_key1 %s' % p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    if row['tst_c03'] in ret[row['tst_c01']][row['tst_c02']]:
                        pass
                    else:
                        ret[row['tst_c01']][row['tst_c02']].update({row['tst_c03']: row})
                else:
                    ret[row['tst_c01']].update({row['tst_c02']: {row['tst_c03']: row}})
            else:
                ret.update({row['tst_c01']: {row['tst_c02']: {row['tst_c03']: row}}})

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0(p_count):
        return StaticDataLayer.execute_singleton0('exec dbo.tst_test_singleton0 %s' % p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1(p_count):
        return StaticDataLayer.execute_singleton1('exec dbo.tst_test_singleton1 %s' % p_count)


# ----------------------------------------------------------------------------------------------------------------------
