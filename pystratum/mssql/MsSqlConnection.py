from pystratum.mssql.StaticDataLayer import StaticDataLayer
from pystratum import Connection


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlConnection(Connection.Connection):
    """
    Class for connecting to SQL Server instances and reading SQl Server specific connection parameters from
    configuration files.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._host_name = None
        """
        The hostname of the SQL Server instance.

        :type: string
        """

        self._user_name = None
        """
        User name.

        :type: string
        """

        self._password = None
        """
        Password required for singing on to the SQL Server instance.

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
    def _read_configuration_file(self, filename: str):
        """
        Reads parameters from the configuration file. Checks the supplement files, and sets values to attributes
        of class.

        :param str filename: The path to the configuration file.
        """
        config, config_supplement = self._read_configuration(filename)

        self._host_name = self._get_option(config, config_supplement, 'database', 'host_name')
        self._user_name = self._get_option(config, config_supplement, 'database', 'user_name')
        self._password = self._get_option(config, config_supplement, 'database', 'password')
        self._database = self._get_option(config, config_supplement, 'database', 'database_name')


# ----------------------------------------------------------------------------------------------------------------------
