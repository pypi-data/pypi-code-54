__version__ = "0.1.0"

import json
import urllib.request

BASE_API_URL = "https://gpdf.io/api"


class ApiError(Exception):
    pass


class Response:
    def __init__(self, status=200, success=True, message=None):
        self.status = status
        self.success = success
        self.message = message

        if self.message is None:
            raise ApiError("Empty response message")

    def get_url(self):
        return "{}/files/{}?hash={}".format(
            BASE_API_URL, self.message["id"], self.message["file_hash"]
        )

    def save_pdf(self, filename):
        return urllib.request.urlretrieve(self.get_url(), filename)


class GpdfApi:
    def __init__(self, api_key):
        """GPdf Api Wrapper"""
        self.api_key = api_key

    def send_request(self, app_slug, **kwargs):
        """
        Sends a request to generate a new pdf for specific app slug
        with optional arguments.

        Raises urllib.error.URLError in event of error
        """
        query = [{"name": name, "value": value} for name, value in kwargs.items()]

        data = {"slug": app_slug, "query": query}

        req = urllib.request.Request(
            "{}/files".format(BASE_API_URL),
            method="POST",
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Python SDK/{}".format(__version__),
                "gpdf-access-token": self.api_key,
            },
        )

        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode("utf-8"))
            return Response(**result)
