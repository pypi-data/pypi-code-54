import argparse

from rockart_examples import __version__, RockartExamplesException
from rockart_examples.life.gui import run_gui


def entry():
    parser = \
        argparse.ArgumentParser(
            description="Conway's Game of Life - Rockart usage example"
        )
    if __version__ is not None:
        parser.add_argument(
            "-v", "--version",
            action="version",
            version=__version__,
            help="show version of Rockart Examples and exit"
        )
    parser.parse_args()

    try:
        run_gui()
    except RockartExamplesException as e:
        return str(e)
    except:  # noqa
        return "Unknown error occurred"
