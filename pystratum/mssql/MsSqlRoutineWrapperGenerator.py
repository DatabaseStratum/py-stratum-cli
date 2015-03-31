from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator
from pystratum.mssql.wrapper import create_routine_wrapper


# ----------------------------------------------------------------------------------------------------------------------
class MsSqlRoutineWrapperGenerator(RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """
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
