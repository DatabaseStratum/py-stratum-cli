"""
PyStratum
"""
from pystratum.wrapper.Wrapper import Wrapper


class LogWrapper(Wrapper):
    """
    Wrapper method generator for stored procedures with designation type log.
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

# ----------------------------------------------------------------------------------------------------------------------
