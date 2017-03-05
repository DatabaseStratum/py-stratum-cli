"""
PyStratum
"""
from pystratum.wrapper.Wrapper import Wrapper


class BulkWrapper(Wrapper):
    """
    Wrapper method generator for stored procedures with designation type bulk.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self):
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return 'int'

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_wrapper_args(routine):
        ret = 'bulk_handler'

        if routine['parameters']:
            ret += ', '

        return ret + Wrapper._get_wrapper_args(routine)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_docstring_parameters(self, routine):
        self._write_line('')
        self._write_line(':param pystratum.BulkHandler.BulkHandler bulk_handler: The bulk handler for processing the selected rows.')

        Wrapper._write_docstring_parameters(self, routine)


# ----------------------------------------------------------------------------------------------------------------------
