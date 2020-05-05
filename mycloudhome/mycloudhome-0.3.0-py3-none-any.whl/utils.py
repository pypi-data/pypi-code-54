import json
import os
from pathlib import Path

import requests

import mycloudhome.configure as configure
import mycloudhome.authorization as auth
import mycloudhome.filemanagement as filemanagement

from collections import OrderedDict
from pprint import pformat


def load_json_preserve_order(s):
    return json.loads(s, object_pairs_hook=OrderedDict)


def pretty(d: dict):
    return pformat(d)


# wd:// --> root
# wd://temp/a.txt --> some file id
def convert_wd_path_to_wd_id(wdPath):
    if wdPath == 'wd://' or wdPath == 'root':
        return 'root'
    idx = 'root'
    for name in wdPath.replace("wd://", "").split('/'):
        if name == "":
            continue
        sub_dir = filemanagement.get_file_under_dir_by_name(name, idx)
        if sub_dir is None:
            raise Exception("WD PATH Not FOUND!!! [{}]".format(name))
        idx = sub_dir['id']

    if configure.debug:
        print("Convert {} to {}".format(wdPath, idx))
    return idx


def is_wd_path(path):
    if path.startswith('wd://'):
        return True
    if path == 'root':
        return True
    return False


def is_local_dir(path):
    return Path(path).is_dir()

def is_local_file(path):
    return Path(path).is_file()

def get_local_file_name(path):
    return Path(path).name