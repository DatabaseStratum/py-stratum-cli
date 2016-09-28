"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class DataTypeHelper(metaclass=abc.ABCMeta):
    """
    Utility class for deriving information based on a DBMS native data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def column_type_to_python_type(self, data_type_info):
        """
        Returns the corresponding Python data type of a DBMS native data type.

        :param dict data_type_info: The DBMS native data type metadata.

        :rtype: str
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
