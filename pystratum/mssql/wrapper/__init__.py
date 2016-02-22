from pystratum.mssql.wrapper.FunctionsWrapper import FunctionsWrapper
from pystratum.mssql.wrapper.LogWrapper import LogWrapper
from pystratum.mssql.wrapper.NoneWrapper import NoneWrapper
from pystratum.mssql.wrapper.Row0Wrapper import Row0Wrapper
from pystratum.mssql.wrapper.Row1Wrapper import Row1Wrapper
from pystratum.mssql.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper
from pystratum.mssql.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper
from pystratum.mssql.wrapper.RowsWrapper import RowsWrapper
from pystratum.mssql.wrapper.Singleton0Wrapper import Singleton0Wrapper
from pystratum.mssql.wrapper.Singleton1Wrapper import Singleton1Wrapper


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_wrapper(routine, lob_as_string_flag):
    """
    A factory for creating the appropriate object for generating a wrapper method for a stored routine.
    :return:
    """
    if routine['designation'] == 'none':
        wrapper = NoneWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row0':
        wrapper = Row0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row1':
        wrapper = Row1Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows':
        wrapper = RowsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_index':
        wrapper = RowsWithIndexWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_key':
        wrapper = RowsWithKeyWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton0':
        wrapper = Singleton0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton1':
        wrapper = Singleton1Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'function':
        wrapper = FunctionsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'log':
        wrapper = LogWrapper(routine, lob_as_string_flag)
    # elif routine['designation'] == 'table':
    #     wrapper = TableWrapper(routine, lob_as_string_flag)
    # elif routine['designation'] == 'bulk':
    #     wrapper = BulkWrapper(routine, lob_as_string_flag)
    # elif routine['designation'] == 'bulk_insert':
    #     wrapper = BulkInsertWrapper(routine, lob_as_string_flag)
    else:
        raise Exception("Unknown routine type '{0!s}'.".format(routine['designation']))

    return wrapper


# ----------------------------------------------------------------------------------------------------------------------
