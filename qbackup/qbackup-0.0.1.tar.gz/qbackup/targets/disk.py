""" disk as task target """

from qbackup.target import Target
from py_json_serialize import json_serialize

class Disk(Target):
    """ local disk as target target """
    pass

@json_serialize
class FileTarget(Disk):
    name = ""
    """ target file """
    def __init__(self, name = ""):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name