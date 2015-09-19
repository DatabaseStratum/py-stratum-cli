import configparser
from pystratum.mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MySqlConnection:
    """
    Class for connecting to MySQL instances and reading MySQL specific connection parameters from configuration files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._host_name = None
        """
        The hostname of the MySQL instance.

        :type: string
        """

        self._port = None
        """
        The port of the MySQL instance.

        :type: string
        """

        self._user_name = None
        """
        User name.

        :type: string
        """

        self._password = None
        """
        Password required for logging in on to the MySQL instance.

        :type: string
        """

        self._database = None
        """
        The database name.

        :type: string
        """

        self._character_set_client = None
        """
        The default character set under which the stored routine will be loaded and run.

        :type: string
        """

        self._collation_connection = None
        """
        The default collate under which the stored routine will be loaded and run.

        :type: string
        """

        self._sql_mode = None
        """
        The SQL mode under which the stored routine will be loaded and run.

        :type: string
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the MySQL instance.
        """
        StaticDataLayer.config['database'] = self._database
        StaticDataLayer.config['user'] = self._user_name
        StaticDataLayer.config['password'] = self._password
        StaticDataLayer.config['host'] = self._host_name
        StaticDataLayer.config['port'] = self._port
        StaticDataLayer.config['charset'] = self._character_set_client
        StaticDataLayer.config['collation'] = self._collation_connection
        StaticDataLayer.config['sql_mode'] = self._sql_mode

        StaticDataLayer.connect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the MySQL instance.
        """
        StaticDataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._database = config.get('database', 'database_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._host_name = config.get('database', 'host_name', fallback='localhost')
        self._port = int(config.get('database', 'port', fallback='3306'))
        self._character_set_client = config.get('database', 'character_set_client', fallback='utf-8')
        self._collation_connection = config.get('database', 'collation_connection', fallback='utf8_general_ci')
        self._sql_mode = config.get('database', 'sql_mode')


# ----------------------------------------------------------------------------------------------------------------------
