"""
PyStratum
"""
import abc
import math
import os
import re
import stat

from pystratum.DocBlockReflection import DocBlockReflection
from pystratum.exception.LoaderException import LoaderException


class RoutineLoaderHelper(metaclass=abc.ABCMeta):
    """
    Class for loading a single stored routine into a RDBMS instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 routine_filename,
                 routine_file_encoding,
                 pystratum_old_metadata,
                 replace_pairs,
                 rdbms_old_metadata,
                 io):
        """
        Object constructor.

        :param str routine_filename: The filename of the source of the stored routine.
        :param str routine_file_encoding: The encoding of the source file.
        :param dict pystratum_old_metadata: The metadata of the stored routine from PyStratum.
        :param dict[str,str] replace_pairs: A map from placeholders to their actual values.
        :param dict rdbms_old_metadata: The old metadata of the stored routine from MS SQL Server.
        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        self._source_filename = routine_filename
        """
        The source filename holding the stored routine.

        :type: str
        """

        self._routine_file_encoding = routine_file_encoding
        """
        The encoding of the routine file.
        """

        self._pystratum_old_metadata = pystratum_old_metadata
        """
        The old metadata of the stored routine.  Note: this data comes from the metadata file.

        :type: dict
        """

        self._pystratum_metadata = {}
        """
        The metadata of the stored routine. Note: this data is stored in the metadata file and is generated by
        pyStratum.

        :type: dict
        """

        self._replace_pairs = replace_pairs
        """
        A map from placeholders to their actual values.

        :type: dict
        """

        self._rdbms_old_metadata = rdbms_old_metadata
        """
        The old information about the stored routine. Note: this data comes from the metadata of the RDBMS instance.

        :type: dict
        """

        self._m_time = 0
        """
        The last modification time of the source file.

        :type: int
        """

        self._routine_name = None
        """
        The name of the stored routine.

        :type: str
        """

        self._routine_source_code = None
        """
        The source code as a single string of the stored routine.

        :type: str
        """

        self._routine_source_code_lines = []
        """
        The source code as an array of lines string of the stored routine.

        :type: list
        """

        self._replace = {}
        """
        The replace pairs (i.e. placeholders and their actual values).
        :type: dict
        """

        self._routine_type = None
        """
        The stored routine type (i.e. procedure or function) of the stored routine.

        :type: str
        """

        self._designation_type = None
        """
        The designation type of the stored routine.

        :type: str
        """

        self._doc_block_parts_source = dict()
        """
        All DocBlock parts as found in the source of the stored routine.

        :type: dict
        """

        self._doc_block_parts_wrapper = dict()
        """
        The DocBlock parts to be used by the wrapper generator.

        :type: dict
        """

        self._columns_types = None
        """
        The column types of columns of the table for bulk insert of the stored routine.

        :type: list
        """

        self._fields = None
        """
        The keys in the dictionary for bulk insert.

        :type: list
        """

        self._parameters = []
        """
        The information about the parameters of the stored routine.

        :type: list[dict]
        """

        self._table_name = None
        """
        If designation type is bulk_insert the table name for bulk insert.

        :type: str
        """

        self._columns = None
        """
        The key or index columns (depending on the designation type) of the stored routine.

        :type: list
        """

        self._io = io
        """
        The output decorator.

        :type: pystratum.style.PyStratumStyle.PyStratumStyle
        """

        self.shadow_directory = None
        """
        The name of the directory were copies with pure SQL of the stored routine sources must be stored.

        :type: str|None
        """

    # ------------------------------------------------------------------------------------------------------------------
    def load_stored_routine(self):
        """
        Loads the stored routine into the instance of MySQL.

        Returns the metadata of the stored routine if the stored routine is loaded successfully. Otherwise returns
        False.

        :rtype: dict[str,str]|bool
        """
        try:
            self._routine_name = os.path.splitext(os.path.basename(self._source_filename))[0]

            if os.path.exists(self._source_filename):
                if os.path.isfile(self._source_filename):
                    self._m_time = int(os.path.getmtime(self._source_filename))
                else:
                    raise LoaderException("Unable to get mtime of file '{}'".format(self._source_filename))
            else:
                raise LoaderException("Source file '{}' does not exist".format(self._source_filename))

            if self._pystratum_old_metadata:
                self._pystratum_metadata = self._pystratum_old_metadata

            load = self._must_reload()
            if load:
                self.__read_source_file()

                self.__get_placeholders()

                self._get_designation_type()

                self._get_name()

                self.__substitute_replace_pairs()

                self._load_routine_file()

                if self._designation_type == 'bulk_insert':
                    self._get_bulk_insert_table_columns_info()

                self._get_routine_parameters_info()

                self.__get_doc_block_parts_wrapper()

                self.__save_shadow_copy()

                self._update_metadata()

            return self._pystratum_metadata

        except Exception as exception:
            self._log_exception(exception)
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def __read_source_file(self):
        """
        Reads the file with the source of the stored routine.
        """
        with open(self._source_filename, 'r', encoding=self._routine_file_encoding) as file:
            self._routine_source_code = file.read()

        self._routine_source_code_lines = self._routine_source_code.split("\n")

    # ------------------------------------------------------------------------------------------------------------------
    def __save_shadow_copy(self):
        """
        Saves a copy of the stored routine source with pure SQL (if shadow directory is set).
        """
        if not self.shadow_directory:
            return

        destination_filename = os.path.join(self.shadow_directory, self._routine_name) + '.sql'

        if os.path.realpath(destination_filename) == os.path.realpath(self._source_filename):
            raise LoaderException("Shadow copy will override routine source '{}'".format(self._source_filename))

        # Remove the (read only) shadow file if it exists.
        if os.path.exists(destination_filename):
            os.remove(destination_filename)

        # Write the shadow file.
        with open(destination_filename, 'wt', encoding=self._routine_file_encoding) as handle:
            handle.write(self._routine_source_code)

        # Make the file read only.
        mode = os.stat(self._source_filename)[stat.ST_MODE]
        os.chmod(destination_filename, mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)

    # ------------------------------------------------------------------------------------------------------------------
    def __substitute_replace_pairs(self):
        """
        Substitutes all replace pairs in the source of the stored routine.
        """
        self._set_magic_constants()

        routine_source = []
        i = 0
        for line in self._routine_source_code_lines:
            self._replace['__LINE__'] = "'%d'" % (i + 1)
            for search, replace in self._replace.items():
                tmp = re.findall(search, line, re.IGNORECASE)
                if tmp:
                    line = line.replace(tmp[0], replace)
            routine_source.append(line)
            i += 1

        self._routine_source_code = "\n".join(routine_source)

    # ------------------------------------------------------------------------------------------------------------------
    def _log_exception(self, exception):
        """
        Logs an exception.

        :param Exception exception: The exception.

        :rtype: None
        """
        self._io.error(str(exception).strip().split(os.linesep))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _must_reload(self):
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.

        :rtype: bool
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __get_placeholders(self):
        """
        Extracts the placeholders from the stored routine source.
        """
        ret = True

        pattern = re.compile('(@[A-Za-z0-9_.]+(%(max-)?type)?@)')
        matches = pattern.findall(self._routine_source_code)

        placeholders = []

        if len(matches) != 0:
            for tmp in matches:
                placeholder = tmp[0]
                if placeholder.lower() not in self._replace_pairs:
                    raise LoaderException("Unknown placeholder '{0}' in file {1}".
                                          format(placeholder, self._source_filename))
                if placeholder not in placeholders:
                    placeholders.append(placeholder)

        for placeholder in placeholders:
            if placeholder not in self._replace:
                self._replace[placeholder] = self._replace_pairs[placeholder.lower()]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_designation_type(self):
        """
        Extracts the designation type of the stored routine.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _is_start_or_store_routine(self, line):
        """
        Returns True if a line is the start of the code of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __get_doc_block_lines(self):
        """
        Returns the start and end line of the DOcBlock of the stored routine code.
        """
        line1 = None
        line2 = None

        i = 0
        for line in self._routine_source_code_lines:
            if re.match(r'\s*/\*\*', line):
                line1 = i

            if re.match(r'\s*\*/', line):
                line2 = i

            if self._is_start_or_store_routine(line):
                break

            i += 1

        return line1, line2

    # ------------------------------------------------------------------------------------------------------------------
    def __get_doc_block_parts_source(self):
        """
        Extracts the DocBlock (in parts) from the source of the stored routine source.
        """
        line1, line2 = self.__get_doc_block_lines()

        if line1 is not None and line2 is not None and line1 <= line2:
            doc_block = self._routine_source_code_lines[line1:line2 - line1 + 1]
        else:
            doc_block = list()

        reflection = DocBlockReflection(doc_block)

        self._doc_block_parts_source['description'] = reflection.get_description()

        self._doc_block_parts_source['parameters'] = list()
        for tag in reflection.get_tags('param'):
            parts = re.match(r'^(@param)\s+(\w+)\s*(.+)?', tag, re.DOTALL)
            if parts:
                self._doc_block_parts_source['parameters'].append({'name':        parts.group(2),
                                                                   'description': parts.group(3)})

    # ------------------------------------------------------------------------------------------------------------------
    def __get_parameter_doc_description(self, name):
        """
        Returns the description by name of the parameter as found in the DocBlock of the stored routine.

        :param str name: The name of the parameter.

        :rtype: str
        """
        for param in self._doc_block_parts_source['parameters']:
            if param['name'] == name:
                return param['description']

        return ''

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_data_type_helper(self):
        """
        Returns a data type helper object appropriate for the RDBMS.

        :rtype: pystratum.helper.DataTypeHelper.DataTypeHelper
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __get_doc_block_parts_wrapper(self):
        """
        Generates the DocBlock parts to be used by the wrapper generator.
        """
        self.__get_doc_block_parts_source()

        helper = self._get_data_type_helper()

        parameters = list()
        for parameter_info in self._parameters:
            parameters.append(
                {'parameter_name':       parameter_info['name'],
                 'python_type':          helper.column_type_to_python_type(parameter_info),
                 'data_type_descriptor': parameter_info['data_type_descriptor'],
                 'description':          self.__get_parameter_doc_description(parameter_info['name'])})

        self._doc_block_parts_wrapper['description'] = self._doc_block_parts_source['description']
        self._doc_block_parts_wrapper['parameters'] = parameters

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_name(self):
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _load_routine_file(self):
        """
        Loads the stored routine into the RDBMS instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_bulk_insert_table_columns_info(self):
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_routine_parameters_info(self):
        """
        Retrieves information about the stored routine parameters from the meta data of the RDBMS.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _update_metadata(self):
        """
        Updates the metadata of the stored routine.
        """
        self._pystratum_metadata['routine_name'] = self._routine_name
        self._pystratum_metadata['designation'] = self._designation_type
        self._pystratum_metadata['table_name'] = self._table_name
        self._pystratum_metadata['parameters'] = self._parameters
        self._pystratum_metadata['columns'] = self._columns
        self._pystratum_metadata['fields'] = self._fields
        self._pystratum_metadata['column_types'] = self._columns_types
        self._pystratum_metadata['timestamp'] = self._m_time
        self._pystratum_metadata['replace'] = self._replace
        self._pystratum_metadata['pydoc'] = self._doc_block_parts_wrapper

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _drop_routine(self):
        """
        Drops the stored routine if it exists.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _set_magic_constants(self):
        """
        Adds magic constants to replace list.
        """
        real_path = os.path.realpath(self._source_filename)

        self._replace['__FILE__'] = "'%s'" % real_path
        self._replace['__ROUTINE__'] = "'%s'" % self._routine_name
        self._replace['__DIR__'] = "'%s'" % os.path.dirname(real_path)

    # ------------------------------------------------------------------------------------------------------------------
    def _unset_magic_constants(self):
        """
        Removes magic constants from current replace list.
        """
        if '__FILE__' in self._replace:
            del self._replace['__FILE__']

        if '__ROUTINE__' in self._replace:
            del self._replace['__ROUTINE__']

        if '__DIR__' in self._replace:
            del self._replace['__DIR__']

        if '__LINE__' in self._replace:
            del self._replace['__LINE__']

    # ------------------------------------------------------------------------------------------------------------------
    def _print_sql_with_error(self, sql, error_line):
        """
        Writes a SQL statement with an syntax error to the output. The line where the error occurs is highlighted.

        :param str sql: The SQL statement.
        :param int error_line: The line where the error occurs.
        """
        if os.linesep in sql:
            lines = sql.split(os.linesep)
            digits = math.ceil(math.log(len(lines) + 1, 10))
            i = 1
            for line in lines:
                if i == error_line:
                    self._io.text('<error>{0:{width}} {1}</error>'.format(i, line, width=digits, ))
                else:
                    self._io.text('{0:{width}} {1}'.format(i, line, width=digits, ))
                i += 1
        else:
            self._io.text(sql)

# ----------------------------------------------------------------------------------------------------------------------
