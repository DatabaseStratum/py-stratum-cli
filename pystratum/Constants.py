"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
import configparser

from pystratum.Util import Util


class Constants:
    """
    Abstract parent class for RDBMS specific classes for creating constants based on column widths, and auto increment
    columns and labels.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        self._constants = {}
        """
        All constants.

        :type: dict
        """

        self._old_columns = {}
        """
        The previous column names, widths, and constant names (i.e. the content of $myConstantsFilename upon
        starting this program).

        :type: dict
        """

        self._constants_filename = None
        """
        Filename with column names, their widths, and constant names.

        :type: str
        """

        self._prefix = None
        """
        The prefix used for designations a unknown constants.
        :type: str
        """

        self._template_config_filename = None
        """
        Template filename under which the file is generated with the constants.

        :type: str
        """

        self._config_filename = None
        """
        The destination filename with constants.

        :type: str
        """

        self._columns = {}
        """
        All columns in the MySQL schema.

        :type: dict
        """

        self._labels = {}
        """
        All primary key labels, their widths and constant names.

        :type: dict
        """

        self._io = io
        """
        The output decorator.

        :type: pystratum.style.PyStratumStyle.PyStratumStyle
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def connect(self):
        """
        Connects to the database.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def disconnect(self):
        """
        Disconnects from the database.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, config_filename, regex):
        """
        :param str config_filename: The config filename.
        :param str regex: The regular expression for columns which we want to use.

        :rtype: int
        """
        self._read_configuration_file(config_filename)

        if self._constants_filename:
            self._io.title('Constants')

            self.connect()
            self._get_old_columns()
            self._get_columns()
            self._enhance_columns()
            self._merge_columns()
            self._write_columns()
            self._get_labels(regex)
            self._fill_constants()
            self._write_target_config_file()
            self.disconnect()
            self.__log_number_of_constants()
        else:
            self._io.log_verbose('Constants not enabled')

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def __log_number_of_constants(self):
        """
        Logs the number of constants generated.
        """
        n_id = len(self._labels)
        n_widths = len(self._constants) - n_id

        self._io.writeln('')
        self._io.text('Number of constants based on column widths: {0}'.format(n_widths))
        self._io.text('Number of constants based on database IDs : {0}'.format(n_id))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(config_filename)

        self._constants_filename = config.get('constants', 'columns')
        self._prefix = config.get('constants', 'prefix')
        self._template_config_filename = config.get('constants', 'config_template')
        self._config_filename = config.get('constants', 'config')

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_old_columns(self):
        """
        Reads from file constants_filename the previous table and column names, the width of the column,
        and the constant name (if assigned) and stores this data in old_columns.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_columns(self):
        """
        Retrieves metadata all columns in the MySQL schema.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _enhance_columns(self):
        """
        Enhances old_columns as follows:
        If the constant name is *, is is replaced with the column name prefixed by prefix in uppercase.
        Otherwise the constant name is set to uppercase.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _merge_columns(self):
        """
        Preserves relevant data in old_columns into columns.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_columns(self):
        """
        Writes table and column names, the width of the column, and the constant name (if assigned) to
        constants_filename.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_labels(self, regex):
        """
        Gets all primary key labels from the MySQL database.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _fill_constants(self):
        """
        Merges columns and labels (i.e. all known constants) into constants.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _write_target_config_file(self):
        """
        Creates a python configuration file with constants.
        """
        content = ''
        for constant, value in sorted(self._constants.items()):
            content += "{0!s} = {1!s}\n".format(str(constant), str(value))

            # Save the configuration file.
        Util.write_two_phases(self._config_filename, content, self._io)

# ----------------------------------------------------------------------------------------------------------------------
