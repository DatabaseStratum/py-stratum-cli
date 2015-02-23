from lib.stratum.mysql.wrapper.Wrapper import Wrapper


# ----------------------------------------------------------------------------------------------------------------------
class Singleton1Wrapper(Wrapper):
    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_singleton1(%s)' % str(self._generate_command(routine)))


# ----------------------------------------------------------------------------------------------------------------------
