"""
PyStratum
"""
from pystratum.wrapper.Wrapper import Wrapper


class Singleton1Wrapper(Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _return_type_hint(self) -> str:
        """
        Returns the return type hint of the wrapper method.

        :rtype: str
        """
        return 'Any'

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self) -> str:
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return '*'

# ----------------------------------------------------------------------------------------------------------------------
