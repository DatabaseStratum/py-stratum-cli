"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""

from pystratum.helper.DataTypeHelper import DataTypeHelper


class MySqlDataTypeHelper(DataTypeHelper):
    """
    Utility class for deriving information based on a MySQL data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def column_type_to_python_type(self, data_type_info):
        """
        Returns the corresponding Python data type of a MySQL data type.

        :param dict data_type_info: The MySQL data type metadata.

        :rtype: str
        """
        if data_type_info['data_type'] in ['tinyint',
                                           'smallint',
                                           'mediumint',
                                           'int',
                                           'bigint',
                                           'year',
                                           'bit']:
            return 'int'

        if data_type_info['data_type'] == 'decimal':
            return 'int' if data_type_info['numeric_scale'] == 0 else 'float'

        if data_type_info['data_type'] in ['float',
                                           'double']:
            return 'float'

        if data_type_info['data_type'] in ['char',
                                           'varchar',
                                           'time',
                                           'timestamp',
                                           'date',
                                           'datetime',
                                           'enum',
                                           'set',
                                           'tinytext',
                                           'text',
                                           'mediumtext',
                                           'longtext']:
            return 'str'

        if data_type_info['data_type'] in ['varbinary',
                                           'binary',
                                           'tinyblob',
                                           'blob',
                                           'mediumblob',
                                           'longblob', ]:
            return 'bytes'

        raise RuntimeError('Unknown data type {0}'.format(data_type_info['data_type']))

# ----------------------------------------------------------------------------------------------------------------------
