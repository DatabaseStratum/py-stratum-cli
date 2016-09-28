"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.wrapper.Wrapper import Wrapper


class FunctionsWrapper(Wrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self):
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return '*'

# ----------------------------------------------------------------------------------------------------------------------
