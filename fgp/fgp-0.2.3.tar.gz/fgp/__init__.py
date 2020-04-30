import logging
from fgp.controller.client import Client
from fgp.controller.store import Store
from fgp.controller.reference import Reference
from fgp.controller.event import Event
from fgp.controller import ApiClient
from fgp.cli import cli


if __name__ == 'fgp':
    # create logger
    logger = logging.getLogger('fgp')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.info('Configured logger')