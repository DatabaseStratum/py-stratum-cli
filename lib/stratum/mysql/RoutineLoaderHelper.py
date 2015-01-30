import sys


# ----------------------------------------------------------------------------------------------------------------------
class RoutineLoaderHelper:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 routine_filename,
                 routine_file_extension,
                 metadata,
                 replace_pairs,
                 old_routine_info,
                 sql_mode,
                 character_set,
                 collate):

        self._metadata = {}

    # ------------------------------------------------------------------------------------------------------------------
    def load_stored_routine(self):
        try:
            pass

            return self._metadata

        except Exception as e:
            print(e, file=sys.stderr)

            return False

# ----------------------------------------------------------------------------------------------------------------------
