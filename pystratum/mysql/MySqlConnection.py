from pystratum.mysql.StaticDataLayer import StaticDataLayer
from pystratum import Connection


# ----------------------------------------------------------------------------------------------------------------------
class MySqlConnection(Connection.Connection):
    """
    Class for connecting to MySQL instances and reading MySQL specific connection parameters from configuration files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._host = None
        """
        The hostname of the MySQL instance.

        :type: string
        """

        self._port = None
        """
        The port of the MySQL instance.

        :type: string
        """

        self._user = None
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
        StaticDataLayer.config['user'] = self._user
        StaticDataLayer.config['password'] = self._password
        StaticDataLayer.config['host'] = self._host
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
    def _read_configuration_file(self, filename):
        """
        Reads connections parameters from the configuration file.

        :param str filename: The path to the configuration file.
        """
        config, config_supplement = self._read_configuration(filename)

        self._host = self._get_option(config, config_supplement, 'database', 'host_name', fallback='localhost')
        self._user = self._get_option(config, config_supplement, 'database', 'user')
        self._password = self._get_option(config, config_supplement, 'database', 'password')
        self._database = self._get_option(config, config_supplement, 'database', 'database')
        self._port = int(self._get_option(config, config_supplement, 'database', 'port', fallback='3306'))
        self._character_set_client = self._get_option(config, config_supplement, 'database', 'character_set_client',
                                                      fallback='utf-8')
        self._collation_connection = self._get_option(config, config_supplement, 'database', 'collation_connection',
                                                      fallback='utf8_general_ci')
        self._sql_mode = self._get_option(config, config_supplement, 'database', 'sql_mode')

# ----------------------------------------------------------------------------------------------------------------------
