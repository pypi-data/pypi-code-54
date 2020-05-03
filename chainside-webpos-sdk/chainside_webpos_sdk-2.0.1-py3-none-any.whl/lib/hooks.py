import json

from base64 import b64encode

from .constants import *

from sdkboil.hooks import PresendHook, FailureHook, SuccessHook
from sdkboil import headers


class HeadersHook(PresendHook):
    def run(self):
        self.request.headers[API_VERSION_HEADER] = self.context.version


class AuthorizationHook(PresendHook):
    def run(self):
        token = self.context.cache.get(self.context.token_cache_key)
        self.request.headers[headers.AUTHORIZATION] = 'Bearer {}'.format(token)


class AuthenticationHook(PresendHook):
    def run(self):
        client_id = self.context.client_id
        secret = self.context.secret
        basic_header = b64encode('{}:{}'.format(
            client_id, secret).encode()).decode()
        self.request.headers[headers.AUTHORIZATION] = 'Basic {}'.format(
            basic_header)


class RequestIdHook(FailureHook):
    def run(self):
        try:
            response_body = json.loads(self.response.body)
            request_id = response_body.get('request_id')
            self.exception.request_id = request_id
        except Exception:
            # We can't retrieve the request id from the response body
            pass
