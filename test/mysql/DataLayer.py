"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer(StaticDataLayer):

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant01():
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant01()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant02():
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant02()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant03():
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant03()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant04():
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant04()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types01(p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param26, p_param27):
        return StaticDataLayer.execute_sp_none("call tst_parameter_types01(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param26, p_param27)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types02(p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param18, p_param19, p_param20, p_param21, p_param22, p_param23, p_param24, p_param25, p_param26, p_param27):
        return StaticDataLayer.execute_sp_none("call tst_parameter_types02(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param18, p_param19, p_param20, p_param21, p_param22, p_param23, p_param24, p_param25, p_param26, p_param27)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_function(p_a, p_b):
        return StaticDataLayer.execute_singleton1("select tst_test_function(%s, %s)", p_a, p_b)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_log():
        return StaticDataLayer.execute_sp_log("call tst_test_log()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_max_allowed_packet(p_tmp_blob):
        return StaticDataLayer.execute_sp_singleton1("call tst_test_max_allowed_packet(%s)", p_tmp_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none(p_count):
        return StaticDataLayer.execute_sp_none("call tst_test_none(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_none("call tst_test_none_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_percent_symbol():
        return StaticDataLayer.execute_sp_rows("call tst_test_percent_symbol()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a(p_count):
        return StaticDataLayer.execute_sp_row0("call tst_test_row0a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_row0("call tst_test_row0a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a(p_count):
        return StaticDataLayer.execute_sp_row1("call tst_test_row1a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_row1("call tst_test_row1a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1(p_count):
        return StaticDataLayer.execute_sp_rows("call tst_test_rows1(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_rows("call tst_test_rows1_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1(p_count):
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_index1(%s)", p_count)
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
    def tst_test_rows_with_index1_with_lob(p_count, p_blob):
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_index1_with_lob(%s, %s)", p_count, p_blob)
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
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_key1(%s)", p_count)
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
    def tst_test_rows_with_key1_with_lob(p_count, p_blob):
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_key1_with_lob(%s, %s)", p_count, p_blob)
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
    def tst_test_singleton0a(p_count):
        return StaticDataLayer.execute_sp_singleton0("call tst_test_singleton0a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_singleton0("call tst_test_singleton0a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a(p_count):
        return StaticDataLayer.execute_sp_singleton1("call tst_test_singleton1a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_singleton1("call tst_test_singleton1a_with_lob(%s, %s)", p_count, p_blob)


# ----------------------------------------------------------------------------------------------------------------------
