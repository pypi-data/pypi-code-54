"""Main module."""
import re
import inspect
import requests
from urllib.parse import urljoin

from minrest import parser


class GenericClient(object):

    auth = None
    method_index = {}

    def __init__(self, api_url, endpoints):
        assert any([isinstance(endpoints, str), isinstance(endpoints, list)])
        self.api_url = api_url
        self._endpoints = endpoints
        self.__make_endpoint_methods()

    @property
    def endpoints(self):
        return self._endpoints

    @property
    def methods(self):
        return [x for x in dir(self.__class__) if x.endswith('Method')]

    @staticmethod
    def __make_method_name(name):
        name = re.sub('\W', '_', name)
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        return re.sub('_{2,}', '_', name) + '_method'

    def __raw_endpoint(self, method_name):
        if isinstance(self._endpoints, list):
            return self._endpoints[self.method_index[method_name]]
        return self._endpoints

    def __request(self, add_to_endpoint=None, **kwargs):
        [code_context] = inspect.stack()[1][4]
        regexp = re.compile(r"\.(.*?)\(")
        method_name = regexp.search(code_context).group(1)
        raw_endpoint = self.__raw_endpoint(method_name)
        endpoint = urljoin(endpoint, add_to_endpoint) \
            if add_to_endpoint is not None else raw_endpoint
        url = urljoin(self.api_url, endpoint)
        return requests.request(url=url, **kwargs)

    def __make_endpoint_methods(self):
        if isinstance(self._endpoints, list):
            for index, endpoint in enumerate(self._endpoints):
                method_name = self.__make_method_name(endpoint)
                self.method_index.update({method_name: index})
                setattr(self.__class__, method_name, self.__request)
        else:
            method_name = self.__make_method_name(self._endpoints)
            self.method_index.update({method_name: 1})
            setattr(self.__class__, method_name, self.__request)