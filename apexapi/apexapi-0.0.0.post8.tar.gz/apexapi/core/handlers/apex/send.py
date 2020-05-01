import json
from munch import munchify

def ok(req, res):
    """ send status ok """
    res.json["status"] = "OK"
    res.data = "OK"