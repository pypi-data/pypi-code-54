from typing import Optional, Dict, Callable

import backoff
from google.oauth2 import _client as _oauth2_client
from google.auth.transport.requests import Request as _GoogleRequest
from google.auth import exceptions as _auth_exceptions
from google.oauth2.service_account import Credentials as _Credentials
import requests as _requests


_OAUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
_IAM_SCOPE = 'https://www.googleapis.com/auth/iam'


@backoff.on_exception(backoff.expo, (ConnectionError, _auth_exceptions.GoogleAuthError), 5)
def _get_google_open_id_connect_token(url: str, credentials_path: str) -> str:
    """ retrieve a token from the service account metadata service """
    credentials: _Credentials = _Credentials.from_service_account_file(
        credentials_path,
        additional_claims={"target_audience": " ".join([url, _IAM_SCOPE])})
    token = credentials._make_authorization_grant_assertion()
    google_request = _GoogleRequest()
    token_response_data = _oauth2_client._token_endpoint_request(google_request, credentials._token_uri, {
        'assertion': token,
        'grant_type': _oauth2_client._JWT_GRANT_TYPE,
    })
    return token_response_data['id_token']


def request_service(method: str,
                    url: str,
                    credentials_path: str,
                    headers: Optional[Dict] = None,
                    retry_decorator: Callable[[_requests.request], _requests.request] = lambda f: f,
                    auth_enabled: bool = True,
                    **kwargs) -> _requests.Response:
    """ call service while adding a google generated token to it """

    if headers is None:
        headers = {"content-type": "application/json"}
    if auth_enabled:
        google_token = _get_google_open_id_connect_token(url, credentials_path)
        headers.update(Authorization=f'bearer {google_token}')

    @retry_decorator
    def request_with_retries():
        response = _requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response

    return request_with_retries()
