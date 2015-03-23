import csv
import pymssql
import sys


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer:
    _conn = None

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def my_msg_handler(msgstate, severity, srvname, procname, line, msgtext):
        if severity > 0:
            print("Error at line %d: %s" % (line, msgtext.decode("utf-8")), file=sys.stderr)
        else:
            print(msgtext.decode("utf-8"))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(server, user, password, database):
        # Connect to the SQL-Server
        DataLayer._conn = pymssql.connect(server, user, password, database)

        # Install our own message handler.
        DataLayer._conn._conn.set_msghandler(DataLayer.my_msg_handler)

        # Set the default settings.
        cursor = DataLayer._conn.cursor()
        cursor.execute('set nocount on')
        cursor.execute('set ansi_nulls on')
        cursor.close()

        # We are not interested in transaction (but in restartable process steps).
        DataLayer._conn.autocommit(True)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        DataLayer._conn.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql, *params):
        cursor = DataLayer._conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row1(sql, *params):
        cursor = DataLayer._conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton(sql, *params):
        cursor = DataLayer._conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        cursor.close()

        return row[0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_csv(sql, filename):
        # Open the CSV file.
        file = open(filename, 'w')
        csv_file = csv.writer(file, dialect='unix')

        # Run the query.
        cursor = DataLayer._conn.cursor()
        cursor.execute(sql)

        # Store all rows in CSV format in the file.
        for row in cursor:
            csv_file.writerow(row)

        # Close the CSV file and the cursor.
        file.close()
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql, *params):
        cursor = DataLayer._conn.cursor()
        cursor.execute(sql, params)
        cursor.close()

# ----------------------------------------------------------------------------------------------------------------------
