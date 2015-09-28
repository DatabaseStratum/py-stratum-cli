import psycopg2
from psycopg2.extras import RealDictCursor


# ----------------------------------------------------------------------------------------------------------------------
class StaticDataLayer:
    """
    Class for connecting to a PostgreSQL instance and running SQL statements and stored routines.
    """
    # ------------------------------------------------------------------------------------------------------------------
    connection = None
    """
    The connection between Python and the PostgreSQL instance.
    :type : psycopg2.extensions.connection
    """

    sp_log_init = 'stratum_log_init'
    """
    The name of the stored routine that must be run before a store routine with designation type "log".
    :type : str
    """

    sp_log_fetch = 'stratum_log_fetch'
    """
    The name of the stored routine that must be run after a store routine with designation type "log".
    :type : str
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_column_name(cursor):
        """
        Returns a list with column names retrieved from the description of a cursor.

        :param psycopg2.extensions.cursor cursor: The cursor.
        :return: list
        """
        column_names = []
        for column in cursor.description:
            column_names.append(column.name)

        return column_names

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def start_transaction(isolation_level='READ-COMMITTED', readonly=None):
        """
        Starts a transaction.

        :param str isolation_level:
        :param bool readonly:
        :return: None
        """
        StaticDataLayer.connection.set_session(isolation_level, readonly)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def commit():
        """
        Commits the current transaction.
        :return: None
        """
        StaticDataLayer.connection.commit()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def rollback():
        """
        Rolls back the current transaction.
        :return: None
        """
        StaticDataLayer.connection.rollback()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(host, database, schema, user, password, port=5432):
        """
        Connects to a PostgreSQL instance.

        :param str host: The hostname on which the PostgreSQL server is running.
        :param str database:
        :param str schema:
        :param str user:
        :param str password:
        :param int port:
        :return: None
        """
        StaticDataLayer.connection = psycopg2.connect(database=database,
                                                      user=user,
                                                      password=password,
                                                      host=host,
                                                      port=port)
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute('set search_path to %s;', (schema,))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the PostgreSQL instance.
        :return: None
        """
        StaticDataLayer.connection.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql, *params):
        """
        Executes a query that does not select any rows.

        :param string sql: The SQL statement.
        :param tuple params: The values for the statement.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql, *params):
        """
        Executes a query that selects 0 or more rows.

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.
        :return list[dict]: The selected rows (an empty list if no rows are selected).
        """
        cursor = StaticDataLayer.connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_none(sql, *params):
        """
        Executes a stored procedure that does not select any rows.

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row0(sql, *params):
        """
        Executes a stored procedure that selects 0 or 1 row.

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.
        :return None|dict: The selected row or None.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        rows = portal.fetchall()
        n = len(rows)
        if n == 1:
            column_names = StaticDataLayer._get_column_name(portal)
            ret = dict(zip(column_names, rows[0]))
        else:
            ret = None
        portal.close()
        cursor.close()

        if not (n == 0 or n == 1):
            raise Exception("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row1(sql, *params):
        """
        Executes a stored procedure that selects 1 row.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return dict: The selected row.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        rows = portal.fetchall()
        column_names = StaticDataLayer._get_column_name(portal)
        n = len(rows)
        if n == 1:
            column_names = StaticDataLayer._get_column_name(portal)
            ret = dict(zip(column_names, rows[0]))
        else:
            ret = None  # Keep our IDE happy.
        portal.close()
        cursor.close()

        if n != 1:
            raise Exception("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_rows(sql, *params):
        """
        Executes a stored procedure that selects 0 or more rows.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return list[disc]: The selected rows (an empty list if no rows are selected).
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        tmp = portal.fetchall()
        column_names = StaticDataLayer._get_column_name(portal)
        portal.close()
        cursor.close()

        ret = []
        for row in tmp:
            ret.append(dict(zip(column_names, row)))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton0(sql, *params):
        """
        Executes a stored procedure that selects 0 or 1 row with 1 column.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return T|None: The value of selected column or None.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        rows = portal.fetchall()
        n = len(rows)
        if n == 1:
            ret = rows[0][0]
        else:
            ret = None  # Keep our IDE happy.
        portal.close()
        cursor.close()

        if not (n == 0 or n == 1):
            raise Exception("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton1(sql: str, *params):
        """
        Executes query that selects 1 row with 1 column.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return T: The value of the selected column.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        n = cursor.rowcount
        if n == 1:
            ret = cursor.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        cursor.close()

        if n != 1:
            raise Exception("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton1(sql: str, *params):
        """
        Executes a stored procedure that selects 1 row with 1 column.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return T: The value of the selected column.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.execute(sql, params)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        rows = portal.fetchall()
        n = len(rows)
        if n == 1:
            ret = rows[0][0]
        else:
            ret = None  # Keep our IDE happy.
        portal.close()
        cursor.close()

        if len(rows) != 1:
            raise Exception("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_table(sql: str, *params):
        # todo methods for showing table
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_log(sql, *params):
        """
        Executes a stored procedure with log stements.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.
        :return int: The number of lines in the log.
        """
        cursor = StaticDataLayer.connection.cursor()

        # Create temporary table for logging.
        cursor.callproc(StaticDataLayer.sp_log_init)

        # Execute the stored procedure.
        cursor.execute(sql, params)

        # Fetch the log messages.
        cursor.callproc(StaticDataLayer.sp_log_fetch)
        portal = StaticDataLayer.connection.cursor(cursor.fetchone()[0])
        messages = portal.fetchall()
        portal.close()
        cursor.close()

        # Log the log messages.
        for message in messages:
            print('%s %s' % message)

        return len(messages)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def copy_from(file, table, sep='\t', null='\\N', size=8192, columns=None):
        """
        Read data from the file-like object file appending them to the table named table.

        :param T file: File-like object to read data from. It must have both read() and readline() methods.
        :param str table: Name of the table to copy data into.
        :param str sep: Columns separator expected in the file. Defaults to a tab.
        :param str null: Textual representation of NULL in the file. The default is the two characters string \\N.
        :param int size: Size of the buffer used to read from the file.
        :param iterable columns: Iterable with name of the columns to import. The length and types should match the
                                 content of the file to read. If not specified, it is assumed that the entire table
                                 matches the file structure.
        "return int: The number of rows copied.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.copy_from(file, table, sep, null, size, columns)
        n = cursor.rowcount
        cursor.close()

        return n

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def copy_to(file, table, sep='\t', null='\\N', columns=None):
        """
        Write the content of the table named table to the file-like object file

        :param T file: File-like object to write data into. It must have a write() method.
        :param str table: Name of the table to copy data from.
        :param str sep: Columns separator expected in the file. Defaults to a tab.
        :param str null: Textual representation of NULL in the file. The default is the two characters string \\N.
        :param iterable columns: Iterable with name of the columns to export. If not specified, export all the columns.
        "return int: The number of rows copied.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.copy_to(file, table, sep, null, columns)
        n = cursor.rowcount
        cursor.close()

        return n

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def copy_expert(sql, file, size=8192):
        """
        Submit a user-composed COPY statement.

        :param str sql: The COPY statement to execute.
        :param T file: A file-like object to read or write (according to sql).
        :param int size: Size of the read buffer to be used in COPY FROM.
        "return int: The number of rows copied.
        """
        cursor = StaticDataLayer.connection.cursor()
        cursor.copy_expert(sql, file, size)
        n = cursor.rowcount
        cursor.close()

        return n

# ----------------------------------------------------------------------------------------------------------------------
