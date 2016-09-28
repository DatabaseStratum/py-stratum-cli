"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum.wrapper.Wrapper import Wrapper


class TableWrapper(Wrapper):
    """
    Wrapper method generator for printing the result set of stored procedures in a table format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self):
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return 'int'

# ----------------------------------------------------------------------------------------------------------------------
