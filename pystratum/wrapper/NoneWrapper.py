"""
PyStratum
"""
from pystratum.wrapper.Wrapper import Wrapper


class NoneWrapper(Wrapper):
    """
    Wrapper method generator for stored procedures without any result set.
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
