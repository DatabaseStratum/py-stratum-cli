from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator
from pystratum.mysql.MySqlConnection import MySqlConnection
from pystratum.mysql.wrapper import create_routine_wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MySqlRoutineWrapperGenerator(MySqlConnection, RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """
    def __init__(self):
        MySqlConnection.__init__(self)
        RoutineWrapperGenerator.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        """
        MySqlConnection._read_configuration_file(self, config_filename)
        RoutineWrapperGenerator._read_configuration_file(self, config_filename)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_function(self, routine):
        """
        Generates a complete wrapper method for a stored routine.
        :param  The metadata of the stored routine.
        """
        wrapper = create_routine_wrapper(routine, self._lob_as_string_flag)
        self._code += wrapper.write_routine_method(routine)


# ----------------------------------------------------------------------------------------------------------------------
