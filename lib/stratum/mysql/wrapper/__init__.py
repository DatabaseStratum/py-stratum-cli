from lib.stratum.mysql.wrapper.LogWrapper import LogWrapper
from lib.stratum.mysql.wrapper.FunctionsWrapper import FunctionsWrapper
from lib.stratum.mysql.wrapper.NoneWrapper import NoneWrapper
from lib.stratum.mysql.wrapper.Row0Wrapper import Row0Wrapper
from lib.stratum.mysql.wrapper.Row1Wrapper import Row1Wrapper
from lib.stratum.mysql.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper
from lib.stratum.mysql.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper
from lib.stratum.mysql.wrapper.RowsWrapper import RowsWrapper
from lib.stratum.mysql.wrapper.Singleton0Wrapper import Singleton0Wrapper
from lib.stratum.mysql.wrapper.Singleton1Wrapper import Singleton1Wrapper


# ----------------------------------------------------------------------------------------------------------------------
def create_routine_wrapper(routine, lob_as_string_flag):
    """
    A factory for creating the appropriate object for generating a wrapper method for a stored routine.
    :return:
    """

    wrapper = None

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
    #elif routine['designation'] == 'table':
    #    wrapper = TableWrapper(routine, lob_as_string_flag)
    #elif routine['designation'] == 'bulk':
    #    wrapper = BulkWrapper(routine, lob_as_string_flag)
    #elif routine['designation'] == 'bulk_insert':
    #    wrapper = BulkInsertWrapper(routine, lob_as_string_flag)

    else:
        print("Unknown routine type '%s'." % routine['designation'])

    return wrapper
