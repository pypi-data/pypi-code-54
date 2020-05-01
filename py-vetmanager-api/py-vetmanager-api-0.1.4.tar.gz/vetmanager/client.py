import requests
from interface import implements, Interface
from vetmanager.domain import UrlInterface


class TokenCredentials:

    login: str
    password: str
    app_name: str

    def __init__(self, login: str, password: str, app_name: str):
        self.login = login
        self.password = password
        self.app_name = app_name


class TokenInterface(Interface):
    pass


class Token(implements(TokenInterface)):

    __credentials: TokenCredentials
    __url: UrlInterface

    def __init__(self, credentials: TokenCredentials, url: UrlInterface):
        self.__credentials = credentials
        self.__url = url

    def __str__(self) -> str:
        token_auth_url = str(self.__url) + '/token_auth.php'
        response = requests.post(token_auth_url, data=vars(self.__credentials))
        response_json = response.json()

        if response.status_code == 401:
            raise WrongAuthenticationException(response_json['title'])
        if response.status_code == 500:
            raise Exception(response_json['title'])
        return response_json['data']['token']


class CachedToken(implements(TokenInterface)):

    __token: TokenInterface
    __cache: str

    def __init__(self, host: TokenInterface):
        self.__host = host
        self.__cache = None

    def __str__(self):
        if not self.__cache:
            self.__cache = str(self.__host)
        return self.__cache


class FakeToken(implements(TokenInterface)):

    increment = 0

    def __init__(self):
        pass

    def __str__(self):
        self.increment = self.increment + 1
        return 'token' + str(self.increment)


class WrongAuthenticationException(Exception):
    pass
