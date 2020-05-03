"""
Utility module for pyDataMover
"""
from enum import Enum
import math
from voluptuous import (Schema,
                        MultipleInvalid,
                        Invalid,
                        Required,
                        REMOVE_EXTRA)

class ProgressTypes(Enum):
    """
    Types of available progress callback
    """
    DISPLAY  = 1
    TRACK    = 2
    CALLBACK = 3
    NONE     = 4

class States(Enum):
    """
    Types of Transfer states.
    """
    CREATED  = 1
    STARTED  = 2
    RUNNING  = 3
    PAUSED   = 4
    FINISHED = 5
    FORCEEND = 6
    DONE     = 7
    ABORTED  = 8

class ArgStates(Enum):
    REQUIERD = 1
    OPTIONAL = 2


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


mover_args = dict()

mover_args['file_file'] = Schema({
    Required('name'): str,
    Required('src_dir'): str,
    Required('dst_dir'): str,
    Required('thread_count', default=8): int,
    Required('weight', default=1): int,
    Required('route', default=None): object,
    Required('progress_type', default=ProgressTypes.TRACK):  ProgressTypes
}, extra=REMOVE_EXTRA)

mover_args['file_s3'] = Schema({
    Required('name'): str,
    Required('src_dir'): str,
    Required('thread_count', default=8): int,
    Required('weight', default=1): int,
    Required('route', default=None): object,
    Required('progress_type', default=ProgressTypes.TRACK):  ProgressTypes
}, extra=REMOVE_EXTRA)

mover_args['file_wdt'] = Schema({
    Required('name'): str,
    Required('src_dir'): str,
    Required('uri'): str,
    Required('weight', default=1): int,
    Required('route', default=None): object,
    Required('progress_type', default=ProgressTypes.TRACK):  ProgressTypes
}, extra=REMOVE_EXTRA)

mover_args['wdt_file'] = Schema({
    Required('name'): str,
    Required('dst_dir'): str,
    Required('start_port', default=5555): int,
    Required('thread_count', default=8): int,
    Required('hostname', default=None): str,
}, extra=REMOVE_EXTRA)

def process_mover_args(kwargs, mover_type):
    return mover_args[mover_type](kwargs)
