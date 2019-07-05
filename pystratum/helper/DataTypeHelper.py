"""
PyStratum
"""
import abc
from typing import Dict, Any


class DataTypeHelper(metaclass=abc.ABCMeta):
    """
    Utility class for deriving information based on a DBMS native data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def column_type_to_python_type(self, data_type_info: Dict[str, Any]) -> str:
        """
        Returns the corresponding Python data type of a DBMS native data type.

        :param dict data_type_info: The DBMS native data type metadata.

        :rtype: str
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def column_type_to_python_type_hint(self, data_type_info: Dict[str, Any]) -> str:
        """
        Returns the corresponding Python data type hint of a MySQL data type.

        :param dict data_type_info: The MySQL data type metadata.

        :rtype: str
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
