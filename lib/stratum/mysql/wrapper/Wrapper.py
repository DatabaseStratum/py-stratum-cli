import abc


# ----------------------------------------------------------------------------------------------------------------------
class Wrapper:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, routine):
        # Buffer for generated code.
        """
        :param routine: The metadata of the stored routine.
        """
        self._code = ''

        # The current level of indentation in the generated code.
        self._indent_level = 1

        self._routine = routine

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_routine_wrapper():
        """
        A factory for creating the appropriate object for generating a wrapper method for a stored routine.
        :return:
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_routine_method():
        """
        Generates a complete wrapper method.
        :return: Python code with a routine wrapper.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _write_result_handler(self):
        """
        Generates code for calling the stored routine in the wrapper method.
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
