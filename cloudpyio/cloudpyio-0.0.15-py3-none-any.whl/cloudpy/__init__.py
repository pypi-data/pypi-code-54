import os
import requests
import psutil

from npc_internal import api


def init(apikey=None):
    print('init')
    api.set_apikey(apikey)


def memory_info():
    proc = psutil.Process(os.getpid())
    return proc.memory_info()
