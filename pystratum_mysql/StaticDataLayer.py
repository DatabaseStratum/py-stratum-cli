"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from time import strftime, gmtime

from mysql.connector import MySQLConnection, InterfaceError
from mysql.connector.cursor import MySQLCursorBufferedDict, MySQLCursorBuffered, MySQLCursor

from pystratum.exception.ResultException import ResultException


class StaticDataLayer:
    """
    Class for connecting to a MySQL instance and executing SQL statements. Also, a parent class for classes with
    static wrapper methods for executing stored procedures and functions.
    """
    # ------------------------------------------------------------------------------------------------------------------
    config = {
        'database':  None,
        'user':      '',
        'password':  '',
        'host':      '127.0.0.1',
        'port':      3306,
        'charset':   'utf8',
        'collation': 'utf8_general_ci',
        'sql_mode':  'STRICT_ALL_TABLES'
    }
    """
    The parameters for connection to the MySQL instance. See
    http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html for a complete overview of all
    parameters.

    :type: dict[str,str|int]
    """

    connection = None
    """
    The connection between Python and the MySQL instance.

    :type: mysql.connector.connection.MySQLConnection
    """

    line_buffered = True
    """
    If True log messages from stored procedures with designation type 'log' are line buffered (Note: In python
    sys.stdout is buffered by default).

    :type: bool
    """

    last_sql = None
    """
    The last executed SQL statement.

    :type: str|None
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def commit():
        """
        Commits the current transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-commit.html
        """
        StaticDataLayer.connection.commit()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect():
        """
        Connects to a MySQL instance. See http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        for a complete overview of all possible keys in config.
        """
        StaticDataLayer.connection = MySQLConnection(**StaticDataLayer.config)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the MySQL instance.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-disconnect.html.
        """
        StaticDataLayer.connection.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_multi(sql):
        """
        Executes a multi query that does not select any rows.

        :param str sql: The SQL statements.
        """
        cursor = MySQLCursor(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        for _ in cursor.execute(sql, multi=True):
            pass
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql, *params):
        """
        Executes a query that does not select any rows. Returns the number of affected rows.

        :param str sql: The SQL statement.
        :param iterable params: The values for the statement.

        :rtype: int
        """
        cursor = MySQLCursor(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        cursor.execute(sql, params)
        cursor.close()

        return cursor.rowcount

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql, *params):
        """
        Executes a query that selects 0 or more rows. Returns the selected rows (an empty list if no rows are selected).

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.

        :rtype: list[dict[str,Object]]
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        cursor.execute(sql, *params)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton1(sql, *params):
        """
        Executes SQL statement that selects 1 row with 1 column. Returns the value of the selected column.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: int:
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        cursor.execute(sql, params)
        rowcount = cursor.rowcount
        if rowcount == 1:
            ret = cursor.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_log(sql, *params):
        """
        Executes a stored routine with designation type "log". Returns the number of log messages.

        :param str sql: The SQL statement for calling the stored routine.
        :param iterable params: The arguments for calling the stored routine.

        :rtype: int
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        itr = cursor.execute(sql, params, multi=True)

        rowcount = 0
        try:
            for result in itr:
                rows = result.fetchall()
                if rows is not None:
                    stamp = strftime('%Y-%m-%d %H:%M:%S', gmtime())
                    for row in rows:
                        print(stamp, end='')
                        for field in row:
                            print(' %s' % field, end='')
                        print('', flush=StaticDataLayer.line_buffered)
                        rowcount += 1
        except InterfaceError:
            pass

        cursor.close()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_none(sql, *params):
        """
        Executes a stored routine that does not select any rows. Returns the number of affected rows.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: int
        """
        cursor = MySQLCursor(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        cursor.close()

        return rowcount

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row0(sql, *params):
        """
        Executes a stored procedure that selects 0 or 1 row. Returns the selected row or None.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: None|dict[str,object]
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (rowcount == 0 or rowcount == 1):
            raise ResultException('0 or 1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row1(sql, *params):
        """
        Executes a stored procedure that selects 1 row. Returns the selected row.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: dict[str,object]
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_rows(sql, *params):
        """
        Executes a stored procedure that selects 0 or more rows. Returns the selected rows (an empty list if no rows
        are selected).

        :param str sql: The SQL statement.
        :param iterable params: The arguments for the statement.

        :rtype: list[dict[str,object]]
        """
        cursor = MySQLCursorBufferedDict(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        StaticDataLayer.last_sql = sql
        ret = itr.__next__().fetchall()
        itr.__next__()
        cursor.close()

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton0(sql, *params):
        """
        Executes a stored procedure that selects 0 or 1 row with 1 column. Returns the value of selected column or None.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: object
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        itr = cursor.execute(sql, params, multi=True)
        StaticDataLayer.last_sql = sql
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()[0]
        else:
            ret = None
        itr.__next__()
        cursor.close()

        if not (rowcount == 0 or rowcount == 1):
            raise ResultException('0 or 1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton1(sql, *params):
        """
        Executes a stored routine with designation type "table", i.e a stored routine that is expected to select 1 row
        with 1 column.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The arguments for the stored procedure.

        :rtype: object The value of the selected column.
        """
        cursor = MySQLCursorBuffered(StaticDataLayer.connection)
        StaticDataLayer.last_sql = sql
        itr = cursor.execute(sql, params, multi=True)
        result = itr.__next__()
        rowcount = result.rowcount
        if rowcount == 1:
            ret = result.fetchone()[0]
        else:
            ret = None  # Keep our IDE happy.
        itr.__next__()
        cursor.close()

        if rowcount != 1:
            raise ResultException('1', rowcount, sql)

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_table(sql, *params):
        """
        Executes a stored routine with designation type "table". Returns the number of rows.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The arguments for calling the stored routine.

        :rtype: int
        """
        # todo methods for showing table
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def rollback():
        """
        Rolls back the current transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-rollback.html
        """
        StaticDataLayer.connection.rollback()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def start_transaction(consistent_snapshot=False, isolation_level='READ-COMMITTED', readonly=None):
        """
        Starts a transaction.
        See http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-start-transaction.html

        :param bool consistent_snapshot:
        :param str isolation_level:
        :param bool readonly:
        """
        StaticDataLayer.connection.start_transaction(consistent_snapshot, isolation_level, readonly)

# ----------------------------------------------------------------------------------------------------------------------
