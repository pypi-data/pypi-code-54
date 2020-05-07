"""Main module."""
import re
import inspect
import requests
from urllib.parse import urljoin

from minrest import parser


class GenericClient(object):

    def __init__(self, api_url, endpoint):
        self.api_url = api_url
        self.endpoints = endpoints

    def call(self, endpoint, *args, **kwargs):
        if not self.is_valid_endpoint(endpoint):
            raise ValueError(f'Invalid endpoint: {endpoint}')

        return (
            requests
            .request(
                urljoin(self.api_url, endpoint),
                *args, **kwargs
            )
        )

    def _is_valid_endpoint(self, endpoint):
        return endpoint in self.endpoints