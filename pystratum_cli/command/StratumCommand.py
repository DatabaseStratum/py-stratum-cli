from pystratum_cli.command.BaseCommand import BaseCommand


class StratumCommand(BaseCommand):
    """
    The stratum command: combination of constants, loader, and wrapper commands.

    stratum
        {config_file : The stratum configuration file}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when StratumCommand is activated.
        """
        self._read_config_file(self.input)

        factory = self._create_backend_factory()

        worker = factory.create_constant_worker(self._config, self._io)
        if worker:
            ret = worker.execute()

            if ret != 0:
                return ret

        worker = factory.create_routine_loader_worker(self._config, self._io)
        if worker:
            ret = worker.execute()

            if ret != 0:
                return ret

        worker = factory.create_routine_wrapper_generator_worker(self._config, self._io)
        if worker:
            ret = worker.execute()

            if ret != 0:
                return ret

        self._io.write('')

        return 0

# ----------------------------------------------------------------------------------------------------------------------
