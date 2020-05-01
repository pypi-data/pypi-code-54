import unittest
from unittest import mock
from vetmanager.domain import FakeUrl
from vetmanager.client import \
    Token, TokenCredentials, WrongAuthenticationException, \
    CachedToken, FakeToken


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestClient(unittest.TestCase):

    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_success(self, mock):
        url = FakeUrl()
        credentials = TokenCredentials(
            login='login',
            password='password',
            app_name='myapp'
        )
        token = Token(credentials=credentials, url=url)
        mock.return_value = MockResponse({
            "status": 200,
            "title": "Authorization completed.",
            "detail": "Авторизация выполнена.",
            "data": {
                "service": "test_app",
                "token": 'test_token',
                'user_id': 1,
            }
        }, 200)
        self.assertEqual(str(token), 'test_token')

    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_wrong_password(self, mock):
        url = FakeUrl()
        credentials = TokenCredentials(
            login='login',
            password='password',
            app_name='myapp'
        )
        token = Token(credentials=credentials, url=url)
        mock.return_value = MockResponse({
            "status": 401,
            "title":  "Wrong authentification.",
            "detail": "Error Message"
        }, 401)
        with self.assertRaises(WrongAuthenticationException):
            str(token)

    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_execution_problem(self, mock):
        url = FakeUrl()
        credentials = TokenCredentials(
            login='login',
            password='password',
            app_name='myapp'
        )
        token = Token(credentials=credentials, url=url)
        mock.return_value = MockResponse({
            "status": 500,
            "title":  "Wrong authentification.",
            "detail": "Error Message"
        }, 500)
        with self.assertRaises(Exception):
            str(token)

    def test_cached_token(self):
        cached = CachedToken(FakeToken())
        self.assertEqual(str(cached), 'token1')
        self.assertEqual(str(cached), 'token1')


if __name__ == '__main__':
    unittest.main()
