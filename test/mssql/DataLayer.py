from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer(StaticDataLayer):

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant02():
        return StaticDataLayer.execute_singleton1('exec [dbo].[tst_magic_constant02]')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant03():
        return StaticDataLayer.execute_singleton1('exec [dbo].[tst_magic_constant03]')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant04():
        return StaticDataLayer.execute_singleton1('exec [dbo].[tst_magic_constant04]')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types01(p_tst_bigint, p_tst_binary, p_tst_bit, p_tst_char, p_tst_date, p_tst_datetime, p_tst_datetime2, p_tst_datetimeoffset, p_tst_decimal, p_tst_float, p_tst_int, p_tst_money, p_tst_nchar, p_tst_numeric, p_tst_nvarchar, p_tst_real, p_tst_smalldatetime, p_tst_smallint, p_tst_smallmoney, p_tst_time, p_tst_tinyint, p_tst_varbinary, p_tst_varchar):
        return StaticDataLayer.execute_none('exec [dbo].[tst_parameter_types01] %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s', p_tst_bigint, p_tst_binary, p_tst_bit, p_tst_char, p_tst_date, p_tst_datetime, p_tst_datetime2, p_tst_datetimeoffset, p_tst_decimal, p_tst_float, p_tst_int, p_tst_money, p_tst_nchar, p_tst_numeric, p_tst_nvarchar, p_tst_real, p_tst_smalldatetime, p_tst_smallint, p_tst_smallmoney, p_tst_time, p_tst_tinyint, p_tst_varbinary, p_tst_varchar)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types02(tst_bigint, tst_int, tst_smallint, tst_tinyint, tst_bit, tst_money, tst_smallmoney, tst_decimal, tst_numeric, tst_float, tst_real, tst_date, tst_datetime, tst_datetime2, tst_datetimeoffset, tst_smalldatetime, tst_time, tst_char, tst_varchar, tst_text, tst_nchar, tst_nvarchar, tst_ntext, tst_binary, tst_varbinary, tst_image, tst_xml):
        return StaticDataLayer.execute_none('exec [dbo].[tst_parameter_types02] %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s', tst_bigint, tst_int, tst_smallint, tst_tinyint, tst_bit, tst_money, tst_smallmoney, tst_decimal, tst_numeric, tst_float, tst_real, tst_date, tst_datetime, tst_datetime2, tst_datetimeoffset, tst_smalldatetime, tst_time, tst_char, tst_varchar, tst_text, tst_nchar, tst_nvarchar, tst_ntext, tst_binary, tst_varbinary, tst_image, tst_xml)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_function(p_a, p_b):
        return StaticDataLayer.execute_singleton1('select [dbo].[tst_test_function](%s, %s)', p_a, p_b)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0(p_count):
        return StaticDataLayer.execute_row0('exec [dbo].[tst_test_row0] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1(p_count):
        return StaticDataLayer.execute_row1('exec [dbo].[tst_test_row1] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows(p_count):
        return StaticDataLayer.execute_rows('exec [dbo].[tst_test_rows] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1(p_count):
        ret = {}
        rows = StaticDataLayer.execute_rows('exec [dbo].[tst_test_rows_with_index1] %s', p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    ret[row['tst_c01']][row['tst_c02']].append(row)
                else:
                    ret[row['tst_c01']][row['tst_c02']] = [row]
            else:
                ret[row['tst_c01']] = {row['tst_c02']: [row]}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_key1(p_count):
        ret = {}
        rows = StaticDataLayer.execute_rows('exec [dbo].[tst_test_rows_with_key1] %s', p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    if row['tst_c03'] in ret[row['tst_c01']][row['tst_c02']]:
                        raise Exception('Duplicate key for %s.' % str((row['tst_c01'], row['tst_c02'], row['tst_c03'])))
                    else:
                        ret[row['tst_c01']][row['tst_c02']][row['tst_c03']] = row
                else:
                    ret[row['tst_c01']][row['tst_c02']] = {row['tst_c03']: row}
            else:
                ret[row['tst_c01']] = {row['tst_c02']: {row['tst_c03']: row}}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0(p_count):
        return StaticDataLayer.execute_singleton0('exec [dbo].[tst_test_singleton0] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1(p_count):
        return StaticDataLayer.execute_singleton1('exec [dbo].[tst_test_singleton1] %s', p_count)


# ----------------------------------------------------------------------------------------------------------------------
