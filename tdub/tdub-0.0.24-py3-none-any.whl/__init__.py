"""
tW analysis tools
"""

__version__ = "0.0.24"


def setup_logging():
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(name)-15s %(funcName)-22s %(levelname)-8s    %(message)s",
    )
    logging.addLevelName(
        logging.WARNING,
        "\033[1;31m{}\033[1;0m".format(logging.getLevelName(logging.WARNING)),
    )
    logging.addLevelName(
        logging.ERROR, "\033[1;35m{}\033[1;0m".format(logging.getLevelName(logging.ERROR))
    )
    logging.addLevelName(
        logging.INFO, "\033[1;32m{}\033[1;0m".format(logging.getLevelName(logging.INFO))
    )
    logging.addLevelName(
        logging.DEBUG, "\033[1;34m{}\033[1;0m".format(logging.getLevelName(logging.DEBUG))
    )
