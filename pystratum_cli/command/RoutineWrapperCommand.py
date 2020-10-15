from pystratum_cli.command.BaseCommand import BaseCommand


class RoutineWrapperCommand(BaseCommand):
    """
    Command for generating a class with wrapper methods for invoking stored routines in a database instance.

    wrapper
        {config_file : The strum configuration file}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes constants command when StratumCommand is activated.
        """
        self._read_config_file(self.input)

        factory = self._create_backend_factory()
        worker = factory.create_routine_wrapper_generator_worker(self._config, self._io)

        if not worker:
            self._io.title('Wrapper')
            self._io.error('Wrapper command is not implemented by the backend')
            return -1

        return worker.execute()

# ----------------------------------------------------------------------------------------------------------------------
