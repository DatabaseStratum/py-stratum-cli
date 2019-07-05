"""
PyStratum
"""
import abc
from typing import Dict


class BulkHandler(metaclass=abc.ABCMeta):
    """
    Abstract class for handlers for stored routines with large result sets.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def row(self, row: Dict) -> None:
        """
        Will be invoked for each row in the result set.

        :param dict row: A row from the result set.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self) -> None:
        """
        Will be invoked before the first row will be processed.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self) -> None:
        """
        Will be invoked after the last row has been processed.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
