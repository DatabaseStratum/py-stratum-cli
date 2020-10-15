from pystratum_cli.application.StratumApplication import StratumApplication


def main() -> int:
    application = StratumApplication()
    ret = application.run()

    return ret
