from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator
from pystratum.mssql.MsSqlConnection import MsSqlConnection
from pystratum.mssql.wrapper import create_routine_wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlRoutineWrapperGenerator(MsSqlConnection, RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        MsSqlConnection.__init__(self)
        RoutineWrapperGenerator.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str):
        """
        Reads parameters from the configuration file.
        """
        MsSqlConnection._read_configuration_file(self, config_filename)
        RoutineWrapperGenerator._read_configuration_file(self, config_filename)

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
