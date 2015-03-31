import configparser
from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator
from pystratum.mysql.wrapper import create_routine_wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MySqlRoutineWrapperGenerator(RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self):
        """
        Reads parameters from the configuration file.
        """
        RoutineWrapperGenerator._read_configuration_file(self)

        config = configparser.ConfigParser()
        config.read(self._configuration_filename)

        self._sql_mode = config.get('loader', 'sql_mode')
        self._character_set = config.get('loader', 'character_set')
        self._collate = config.get('loader', 'collate')

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_function(self, routine):
        """
        Generates a complete wrapper method for a stored routine.
        :param  The metadata of the stored routine.
        """
        wrapper = create_routine_wrapper(routine, self._lob_as_string_flag)
        # xxx tmp
        if wrapper:
            self._code += wrapper.write_routine_method(routine)


# ----------------------------------------------------------------------------------------------------------------------
