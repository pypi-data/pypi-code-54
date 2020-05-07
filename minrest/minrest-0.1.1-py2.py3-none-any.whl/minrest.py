"""Main module."""
import re
import inspect
import requests
from urllib.parse import urljoin

from minrest import parser

def build_url(api_url, *args):
    api_url = re.sub(r'\/$', '', api_url)
    endpoint = '/'.join(list(map(lambda x: re.sub(r'^\/|\/$', '', x), args)))
    return api_url + '/' + endpoint


class GenericClient(object):

    def __init__(self, api_url, endpoints):
        self.api_url = api_url
        self.endpoints = endpoints

    def call(self, endpoint, *args, **kwargs):
        if not self._is_valid_endpoint(endpoint):
            raise ValueError(f'Invalid endpoint: {endpoint}')

        return requests.request(url=urljoin(self.api_url, endpoint), **kwargs)

    def _is_valid_endpoint(self, endpoint):
        return endpoint in self.endpoints