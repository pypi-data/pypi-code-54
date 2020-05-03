import secrets
import time

import requests

API_HOST = 'http://localhost:8000'

cache = {}
_apikey = None


def random_apikey():
    return 'sandbox'


def set_apikey(set_apikey):
    global _apikey
    print('have: %s, set: %s' % (_apikey, set_apikey))
    if _apikey and set_apikey != _apikey:
        raise Exception('already set api key')
    _apikey = set_apikey


def get_apikey():
    global _apikey
    if not _apikey:
        set_apikey(random_apikey())
    return _apikey


def get_server_url():
    apikey = get_apikey()

    cached_value = cache.get(apikey)
    if cached_value:
        return cached_value

    url = '%s/api/instances/init' % API_HOST
    params = {'apikey': apikey}
    print('params', params)
    resp = requests.post(url, data=params)
    print(resp)
    data = resp.json()
    for i in range(100):
        host = data.get('host')
        status = data.get('status')
        if host and status == 'running':
            break
        print('initializing, host=%s, status=%s' % (host, status))
        host = None
        time.sleep(2)
    if not host:
        raise Exception('unable to get a cloudpy host')
    url = 'http://%s:9090' % host
    print('got url --> %s' % url)
    cache[apikey] = url
    return url
