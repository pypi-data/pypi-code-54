import requests
from vetmanager.domain import UrlInterface


class WrongAuthentificationException(Exception):
    pass


class ExecutionException(Exception):
    pass


class VetmanagerClient:

    __app_name: str
    __url: UrlInterface

    def __init__(self, app_name: str, url: UrlInterface):
        self.__app_name = app_name
        self.__url = url

    def token(self, login: str, password: str) -> str:
        request_data = {
            'login': login,
            'password': password,
            'app_name': self.__app_name
        }
        try:
            token_auth_url = str(self.__url) + '/token_auth.php'
            response = requests.post(token_auth_url, data=request_data)
            response_json = response.json()
        except Exception:
            raise ExecutionException("Invalid response or server unavailable")

        if response.status_code == 401:
            raise WrongAuthentificationException(response_json['title'])
        if response.status_code == 500:
            raise ExecutionException(response_json['title'])
        return response_json['data']['token']
