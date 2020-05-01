''' global settings ''' 

from py_singleton import singleton
from py_json_serialize import json_serialize

@singleton
@json_serialize
class AppConfig:
    """ global settings """
    

@json_serialize
class TaskConfig:
    """ task-specific settings """
    pass