"""
PyStratum
"""
from typing import Any, Dict

from pystratum.wrapper.Wrapper import Wrapper


class BulkWrapper(Wrapper):
    """
    Wrapper method generator for stored procedures with designation type bulk.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _return_type_hint(self) -> str:
        """
        Returns the return type hint of the wrapper method.

        :rtype: str
        """
        return 'int'

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self) -> str:
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return 'int'

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _get_wrapper_args(routine: Dict[str, Any]) -> str:
        """
        Returns code for the parameters of the wrapper method for the stored routine.

        :param dict[str,*] routine: The routine metadata.

        :rtype: str
        """
        ret = 'bulk_handler'

        if routine['parameters']:
            ret += ', '

        return ret + Wrapper._get_wrapper_args(routine)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_docstring_parameters(self, routine: Dict[str, Any]) -> None:
        """
        Writes the parameters part of the docstring for the wrapper method of a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        self._write_line('')
        self._write_line(
            ':param pystratum.BulkHandler.BulkHandler bulk_handler: The bulk handler for processing the selected rows.')

        Wrapper._write_docstring_parameters(self, routine)

# ----------------------------------------------------------------------------------------------------------------------
