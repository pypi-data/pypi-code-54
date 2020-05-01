import logging
import logging.config
import socket

HOSTNAME = socket.gethostname()

def setup_logging(loglevel, logfile=None):
    loglevel = loglevel.upper()

    LOGGING_CONFIG = {
        "version"                 : 1,
        "disable_existing_loggers": False,
        "formatters"              : {
            "default": {
                "format": "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(HOSTNAME),
            },
            "plain"  : {
                "format": "%(message)s",
            },
        },
        "handlers"                : {
            "console"      : {
                "class"    : "logging.StreamHandler",
                "formatter": "default",
            },
            "console_plain": {
                "class"    : "logging.StreamHandler",
                "formatter": "plain",
            },
        },
        "loggers"                 : {
            "paye"             : {
                "handlers" : ["console"],
                "level"    : loglevel,
                "propagate": False,
            },
        },
        "root"                    : {
            "handlers": ["console"],
            "level"   : loglevel,
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)

