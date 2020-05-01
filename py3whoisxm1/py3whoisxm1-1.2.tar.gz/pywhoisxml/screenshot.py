from pywhoisxml.conf import URL_DEFAULTS, get_response
from pywhoisxml.exceptions import PyWhoisException
import requests
import base64
from pywhoisxml.auth import Auth


class Screenshot(Auth):
    def __init__(self, api_key, **kwargs):
        self.code = 27
        super().__init__(api_key, self.code)
        self.url = URL_DEFAULTS.get('screenshot')
        self.params = {
            "apiKey": self.api_key,


        }
        self.params.update(kwargs)
        self.domain_name = kwargs.get('url')

    def download_image(self):
        try:
            response = requests.get(self.url, params=self.params)
            with open(f"{self.domain_name}.jpg", "wb") as f:

                f.write(response.content)

        except Exception as e:
            print(e)
            raise PyWhoisException("Error ou")
