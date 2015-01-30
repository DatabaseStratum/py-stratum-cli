# ----------------------------------------------------------------------------------------------------------------------
class StaticDataLayer:
    # The default character set to be used when sending data from and to the MySQL instance.
    char_set = 'utf-8'

    # The SQL mode of the MySQL instance.
    sql_mode = 'STRICT_ALL_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_AUTO_VALUE_ON_ZERO,' \
               'NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,ONLY_FULL_GROUP_BY'

    # The transaction isolation level.
    transaction_isolation_level = 'READ-COMMITTED'

    # Chunk size when transmitting LOB to the MySQL instance. Must be less than max_allowed_packet.
    chunk_size = None

    # Value of variable max_allowed_packet
    max_allowed_packet = None

    # The connection between Python and the MySQL instance.
    mysql = None

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def begin():
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def commit():
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(hostname='localhost', username='', password='', database='test', port=3306):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(query):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row0(query):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row1(query):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(query):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton0(query):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton1(query):
        pass


# ----------------------------------------------------------------------------------------------------------------------

