import configparser
from pystratum.mssql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlConnection:
    def __init__(self):
        self._host_name = None
        """
        The hostname of the MySQL instance.

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

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the database.
        """
        StaticDataLayer.connect(self._host_name,
                                self._user_name,
                                self._password,
                                self._database)

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self):
        """
        Disconnects from the database.
        """
        StaticDataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        :param config_filename string
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._host_name = config.get('database', 'host_name')
        self._user_name = config.get('database', 'user_name')
        self._password = config.get('database', 'password')
        self._database = config.get('database', 'database_name')


# ----------------------------------------------------------------------------------------------------------------------
