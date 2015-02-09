from mysql.connector import DataError, MySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict, MySQLCursorBuffered, MySQLCursor


# ----------------------------------------------------------------------------------------------------------------------
class StaticDataLayer:
    """
    Class for connecting to a MySQL instance and running SQL statements and stored routines.
    """
    config = {
        'database': None,
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'port': 3306,
        'charset': 'utf8',
        'collation': 'utf8_general_ci',
        'sql_mode': 'STRICT_ALL_TABLES'
    }
    """
    The parameters for connection to the MySQL instance. See
    http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html for a complete overview of all
    parameters.
    :type : dict
    """

    connection = None
    """
    The connection between Python and the MySQL instance.
    :type : MySQLConnection
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def start_transaction(consistent_snapshot: bool=False,
                          isolation_level: str='READ-COMMITTED',
                          readonly: bool=None) -> None:
        """
        Starts a transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-start-transaction.html

        :param consistent_snapshot:
        :param isolation_level:
        :param readonly:
        """
        StaticDataLayer.connection.start_transaction(consistent_snapshot, isolation_level, readonly)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def commit() -> None:
        """
        Commit the current transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-commit.html
        """
        StaticDataLayer.connection.commit()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(config: dict=config) -> None:
        """
        Connects to a MySQL instance. See http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        for a complete overview of all possible keys in config.
        :param config: The connection parameters.
        """
        StaticDataLayer.connection = MySQLConnection(**config)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect() -> None:
        """
        Disconnects from the MySQL instance.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-disconnect.html.
        """
        StaticDataLayer.connection.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql: str, *params) -> int:
        """
        Executes a query that does not select rows.

        :param sql: The SQL statement.
        :param params: The values for the statement.
        :return: The number of affected rows.
        """
        cursor = MySQLCursor(StaticDataLayer.connection)
        cursor.execute(sql, params)
        cursor.close()

        return cursor.rowcount

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql: str, *params) -> list:
        """
        Executes a query that selects 0 or more rows.

        :param sql: The SQL statement.
        :param params: The arguments for the statement.
        :return: The selected rows (an empty list if no rows are selected).
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        cursor.execute(sql, *params)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_none(sql: str, *params) -> int:
        """
        Executes a stored procedure that does not select any rows.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The number of affected rows.
        """
        cursor = MySQLCursor(StaticDataLayer.connection)
        itr = cursor.execute(sql, *params, multi=True)
        result = itr.__next__()
        cursor.close()

        return result.rowcount

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row0(sql: str, *params):
        """
        Executes a stored procedure that selects 0 or 1 row.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The selected row or None.
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        n = result.rowcount
        if n == 1:
            ret = result.fetchone()
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (n == 0 or n == 1):
            raise DataError("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row1(sql: str, *params) -> dict:
        """
        Executes a stored procedure that selects 1 row.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The selected row.
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        n = result.rowcount
        if n == 1:
            ret = result.fetchone()
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if n != 1:
            raise DataError("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_rows(sql: str, *params) -> list:
        """
        Executes a stored procedure that selects 0 or more rows.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The selected rows (an empty list if no rows are selected).
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        ret = itr.__next__().fetchall()
        itr.__next__()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton0(sql, *params):
        """
        Executes a stored procedure that selects 0 or 1 row with 1 column.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The value of selected column or None.
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        n = result.rowcount
        if n == 1:
            ret = result.fetchone()[0]
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (n == 0 or n == 1):
            raise DataError("Number of rows selected by query below is %d. Expected 0 or 1.\n%s" %
                            (n, sql))

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton1(sql: str, *params):
        """
        Executes a stored procedure that selects 1 row with 1 column.

        :param sql: The SQL call the the stored procedure.
        :param params: The arguments for the stored procedure.
        :return: The value of the selected column.
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        n = result.rowcount
        if n == 1:
            ret = result.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if n != 1:
            raise DataError("Number of rows selected by query below is %d. Expected 1.\n%s" %
                            (n, sql))

        return ret

# ----------------------------------------------------------------------------------------------------------------------
