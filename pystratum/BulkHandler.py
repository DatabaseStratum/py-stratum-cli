"""
PyStratum
"""
import abc


class BulkHandler(metaclass=abc.ABCMeta):
    """
    Abstract class for handlers for stored routines with large result sets.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def row(self, row):
        """
        Will be invoked for each row in the result set.

        :param dict row: A row from the result set.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        Will be invoked before the first row will be processed.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self):
        """
        Will be invoked after the last row has been processed.

        :rtype: None
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
