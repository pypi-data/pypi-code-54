import click

import logging
from logging.handlers import RotatingFileHandler

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def entry_point(ctx, debug):
    loglevel = logging.WARNING
    if debug:
        loglevel = logging.DEBUG

    # Declare logger with file logging
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = RotatingFileHandler('scraparser.log',
            maxBytes=4000000,
            backupCount=5)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
