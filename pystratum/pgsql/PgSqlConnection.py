import configparser

from pystratum.pgsql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class PgSqlConnection:
    """
    Class for connecting to PostgreSQL instances and reading PostgreSQL specific connection parameters from 
    configuration files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._host_name = None
        """
        The hostname of the PostgreSQL instance.

        :type: string
        """

        self._port = None
        """
        The port of the PostgreSQL instance.

        :type: string
        """

        self._user_name = None
        """
        User name.

        :type: string
        """

        self._password = None
        """
        Password required for logging in on to the PostgreSQL instance.

        :type: string
        """

        self._database = None
        """
        The database name.

        :type: string
        """

        self._schema = None
        """
        The schema name.

        :type: string
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the PostgreSQL instance.
        """
        StaticDataLayer.connect(self._host_name,
                                self._database,
                                self._schema,
                                self._user_name,
                                self._password,
                                self._port)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the PostgreSQL instance.
        """
        StaticDataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.
        :param str config_filename:
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._database = config.get('database', 'database_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._schema = config.get('database', 'schema')
        self._host_name = config.get('database', 'host_name', fallback='localhost')
        self._port = int(config.get('database', 'port', fallback='5432'))

# ----------------------------------------------------------------------------------------------------------------------
