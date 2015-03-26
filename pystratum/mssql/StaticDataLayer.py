import csv
import pymssql


# ----------------------------------------------------------------------------------------------------------------------
class StaticDataLayer:
    # ------------------------------------------------------------------------------------------------------------------
    __conn = None
    """
    The SQL connection.
    :type: "Object"
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(server, user, password, database):
        # Connect to the SQL-Server
        StaticDataLayer.__conn = pymssql.connect(server, user, password, database)

        # Set the default settings.
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute('set nocount on')
        cursor.execute('set ansi_nulls on')
        cursor.close()

        # We are not interested in transaction (but in restartable process steps).
        StaticDataLayer.__conn.autocommit(True)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        StaticDataLayer.__conn.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0]
        elif n == 0:
            return None
        else:
            raise Exception("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" %
                            (n, sql))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise Exception("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0][0]
        elif n == 0:
            return None
        else:
            raise Exception("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" % (n, sql))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise Exception("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return rows[0][0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_csv(sql, filename):
        # Open the CSV file.
        file = open(filename, 'w')
        csv_file = csv.writer(file, dialect='unix')

        # Run the query.
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql)

        # Store all rows in CSV format in the file.
        for row in cursor:
            csv_file.writerow(row)

        # Close the CSV file and the cursor.
        file.close()
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_log(sql, *params):
        # todo methods for showing log
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_table(sql: str, *params):
        # todo methods for showing table
        pass


# ----------------------------------------------------------------------------------------------------------------------
