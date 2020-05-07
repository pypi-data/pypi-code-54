import json
import logging
import webbrowser
from typing import AnyStr, NoReturn

import requests
from singleton.singleton import Singleton

from pyquire.models.common import StatusCodes


@Singleton
class Credentials:

    def __init__(self, client_id=None,
                 client_secret=None,
                 refresh_token=None,
                 expires_in=None,
                 token_type=None,
                 access_token=None,
                 server_url=None,
                 set_file=False) -> NoReturn:
        self._server_url = server_url or "http://localhost:65010"
        self._set_file = set_file

        if self._set_file:
            try:
                with open(set_file, 'r') as conf:
                    conf = json.loads(conf.read())
                    self._client_id = conf.get("client_id")
                    self._client_secret = conf.get("client_secret")
                    self._refresh_token = conf.get("refresh_token")
                    self._expires_in = conf.get("expires_in")
                    self._token_type = conf.get("token_type")
                    self._access_token = conf.get("access_token")

            except FileNotFoundError:
                self._client_id = client_id
                self._client_secret = client_secret
                self.get_access_token()
        else:
            self._client_id = client_id
            self._client_secret = client_secret
            self._refresh_token = refresh_token
            self._expires_in = expires_in
            self._token_type = token_type
            self._access_token = access_token

            if not self._access_token:
                self.get_access_token()

    @property
    def client_id(self) -> AnyStr:
        return self._client_id

    @property
    def client_secret(self) -> AnyStr:
        return self._client_secret

    @property
    def refresh_token(self) -> AnyStr:
        return self._refresh_token

    @property
    def expires_in(self) -> AnyStr:
        return self._expires_in

    @property
    def token_type(self) -> AnyStr:
        return self._token_type

    @property
    def access_token(self) -> AnyStr:
        return self._access_token

    def get_access_token(self):
        from flask import Flask, request, redirect

        app = Flask(__name__)
        url = f"https://quire.io/oauth?client_id={self._client_id}&redirect_uri={self._server_url}/callback"

        @app.route('/callback')
        def callback():
            error = request.args.get('error', '')

            if error:
                logging.error("Error: " + error)
            state = request.args.get('state', '')

            if state != StatusCodes.SUCCESS:
                # Uh-oh, this request wasn't started by us!
                logging.error("HTTP Error: " + state)

            code = request.args.get('code')
            response = requests.post(url="https://quire.io/oauth/token", data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self._client_id,
                "client_secret": self._client_secret
            })
            response = response.json()
            self._refresh_token = response.get("refresh_token")
            self._expires_in = response.get("expires_in")
            self._token_type = response.get("token_type")
            self._access_token = response.get("access_token")

            if self._set_file:
                with open(self._set_file, 'w') as conf:
                    response["client_id"] = self._client_id
                    response["client_secret"] = self._client_secret
                    json.dump(response, conf, indent=4)

            # We'll change this next line in just a moment
            return redirect(self._server_url + "/shutdown")

        @app.route('/shutdown')
        def shutdown():
            func = request.environ.get('werkzeug.server.shutdown')

            if func is None:
                raise RuntimeError("Not running with the Werkzeug Server")
            func()

            return "Code received! You can close the tab!"

        webbrowser.open(url)
        app.run(port=65010)

    def refresh_token(self):
        response = requests.post(url="https://quire.io/oauth/token", data={
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret
        })
        response = response.json()
        self._refresh_token = response.get("refresh_token")
        self._expires_in = response.get("expires_in")
        self._token_type = response.get("token_type")
        self._access_token = response.get("access_token")

        if self._set_file:
            with open(self._set_file, 'w') as conf:
                response["client_id"] = self._client_id
                response["client_secret"] = self._client_secret
                json.dump(response, conf, indent=4)
