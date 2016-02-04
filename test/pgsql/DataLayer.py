from pystratum.pgsql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer(StaticDataLayer):

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant01():
        return StaticDataLayer.execute_sp_singleton1("select tst_magic_constant01()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant02():
        return StaticDataLayer.execute_sp_singleton1("select tst_magic_constant02()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant03():
        return StaticDataLayer.execute_sp_singleton1("select tst_magic_constant03()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant04():
        return StaticDataLayer.execute_sp_singleton1("select tst_magic_constant04()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types01(p_tst_bigint, p_tst_int, p_tst_smallint, p_tst_bit, p_tst_money, p_tst_numeric, p_tst_float, p_tst_real, p_tst_date, p_tst_timestamp, p_tst_time6, p_tst_char, p_tst_varchar):
        return StaticDataLayer.execute_sp_none("select tst_parameter_types01(%s::bigint, %s::int, %s::smallint, %s::bit(4), %s::money, %s::numeric, %s::numeric, %s::real, %s::date, %s::timestamp, %s::timestamp, %s::char, %s::varchar)", p_tst_bigint, p_tst_int, p_tst_smallint, p_tst_bit, p_tst_money, p_tst_numeric, p_tst_float, p_tst_real, p_tst_date, p_tst_timestamp, p_tst_time6, p_tst_char, p_tst_varchar)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types02(p_tst_bigint, p_tst_int, p_tst_smallint, p_tst_bit, p_tst_money, p_tst_numeric, p_tst_float, p_tst_real, p_tst_date, p_tst_timestamp, p_tst_time6, p_tst_char, p_tst_varchar, p_tst_text, p_tst_bytea):
        return StaticDataLayer.execute_sp_none("select tst_parameter_types02(%s::bigint, %s::int, %s::smallint, %s::bit(4), %s::money, %s::numeric, %s::numeric, %s::real, %s::date, %s::timestamp, %s::timestamp, %s::char, %s::varchar, %s::text, %s::bytea)", p_tst_bigint, p_tst_int, p_tst_smallint, p_tst_bit, p_tst_money, p_tst_numeric, p_tst_float, p_tst_real, p_tst_date, p_tst_timestamp, p_tst_time6, p_tst_char, p_tst_varchar, p_tst_text, p_tst_bytea)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_big_int(p_bigint):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_big_int(%s::bigint)", p_bigint)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_bit(p_bit):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_bit(%s::bit(4))", p_bit)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_bool(p_bool):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_bool(%s::bool)", p_bool)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_bytea(p_bytea):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_bytea(%s::bytea)", p_bytea)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_char(p_char):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_char(%s::char)", p_char)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_date(p_date):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_date(%s::date)", p_date)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_int(p_int):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_int(%s::int)", p_int)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_money(p_money):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_money(%s::money)", p_money)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_numeric(p_num):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_numeric(%s::numeric)", p_num)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_real(p_real):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_real(%s::real)", p_real)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_small_int(p_smallint):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_small_int(%s::smallint)", p_smallint)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_text(p_txt):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_text(%s::text)", p_txt)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_timestamp(p_ts):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_timestamp(%s::timestamp)", p_ts)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_argument_varchar(p_varchar):
        return StaticDataLayer.execute_singleton1("select tst_test_argument_varchar(%s::varchar)", p_varchar)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_function(p_a, p_b):
        return StaticDataLayer.execute_singleton1("select tst_test_function(%s::int, %s::int)", p_a, p_b)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_log():
        return StaticDataLayer.execute_sp_log("select tst_test_log()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none(p_count):
        return StaticDataLayer.execute_sp_none("select tst_test_none(%s::bigint)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_none("select tst_test_none_with_lob(%s::bigint, %s::bytea)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_percent_symbol():
        return StaticDataLayer.execute_sp_rows("select tst_test_percent_symbol()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a(p_count):
        return StaticDataLayer.execute_sp_row0("select tst_test_row0a(%s::int)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_row0("select tst_test_row0a_with_lob(%s::int, %s::bytea)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a(p_count):
        return StaticDataLayer.execute_sp_row1("select tst_test_row1a(%s::int)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_row1("select tst_test_row1a_with_lob(%s::int, %s::bytea)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1(p_count):
        return StaticDataLayer.execute_sp_rows("select tst_test_rows1(%s::int)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_rows("select tst_test_rows1_with_lob(%s::int, %s::bytea)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1(p_count):
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("select tst_test_rows_with_index1(%s::int)", p_count)
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
        rows = StaticDataLayer.execute_sp_rows("select tst_test_rows_with_index1_with_lob(%s::int, %s::bytea)", p_count, p_blob)
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
        rows = StaticDataLayer.execute_sp_rows("select tst_test_rows_with_key1(%s::int)", p_count)
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
        rows = StaticDataLayer.execute_sp_rows("select tst_test_rows_with_key1_with_lob(%s::int, %s::bytea)", p_count, p_blob)
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
        return StaticDataLayer.execute_sp_singleton0("select tst_test_singleton0a(%s::int)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_singleton0("select tst_test_singleton0a_with_lob(%s::int, %s::bytea)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a(p_count):
        return StaticDataLayer.execute_sp_singleton1("select tst_test_singleton1a(%s::int)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a_with_lob(p_count, p_blob):
        return StaticDataLayer.execute_sp_singleton1("select tst_test_singleton1a_with_lob(%s::int, %s::bytea)", p_count, p_blob)


# ----------------------------------------------------------------------------------------------------------------------
