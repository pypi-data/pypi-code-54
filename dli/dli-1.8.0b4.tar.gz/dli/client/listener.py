import base64
import hashlib
import logging
import os
import re
import sys
import threading
import uuid
from urllib.parse import urlsplit, parse_qs, urlunparse, urljoin

import furl
import requests
from flask import Flask, Blueprint, redirect, request, session
from requests.exceptions import ConnectTimeout

from dli.client.components.urls import sam_urls, identity_urls

class _Listener:

    DEFAULT_PORT = 8080
    # running = False
    localhost = "http://localhost"
    values = {}
    _routes = None
    lock = threading.Lock()
    _condition = threading.Condition(lock)

    #disable the flask startup messaging
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @staticmethod
    def setup_verifiers(code):
        code_verifier = base64.urlsafe_b64encode(code).decode(
            'utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode(
            'utf-8')
        code_challenge = code_challenge.replace('=', '')
        return code_challenge, code_verifier

    @staticmethod
    def run(port=DEFAULT_PORT, debug=False):
        postbox = base64.urlsafe_b64encode(uuid.uuid4().bytes)\
            .decode('utf-8').replace('=', '')

        if not _Listener._routes:
            app = Flask(__name__)
            app.logger.disabled = True
            app.secret_key = os.urandom(20)
            if debug:
                _Listener.app = app

            localhost = f"{_Listener.localhost}:{port}"
            _Listener._routes = Blueprint("auth", __name__, )

            @_Listener._routes.route('/login', methods=['GET'])
            def login():
                postbox = request.args.get("postbox")
                if not postbox:
                    return """
                      <img style="max-width: 300px; height: auto; "
                        src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg" 
                        alt="IHS Logo"
                      >
                      </hr>
                      <h2 style="font-family: Arial, Helvetica, sans-serif;">
                      Forbidden. 
                      </h2>
                    """, 403

                try:
                    # setup the session
                    rnd = os.urandom(40)
                    session["catalogue"] = request.args.get("catalogue")
                    session["sam_client"] = request.args.get("sam_client")
                    session["sam"] = request.args.get("sam")
                    session["code_challenge"], session["code_verifier"] = \
                        _Listener.setup_verifiers(rnd)
                    session["postbox"] = str(postbox)

                    response = requests.head(
                        urljoin(session["catalogue"], "login"),
                        timeout=10
                    )
                    bits = urlsplit(response.headers["Location"])
                    params = parse_qs(bits.query)
                    params["redirect_uri"] = [localhost]
                    path = urlunparse((
                        bits.scheme, bits.netloc, bits.path, '', '', ''
                    ))

                    target_builder = furl.furl(path)

                    target_builder.args = {
                        "state": postbox,
                        "client_id": session["sam_client"],
                        "response_type": "code",
                        "redirect_uri": localhost,
                        "scope": "openid profile saml_attributes email",
                        "code_challenge": session["code_challenge"],
                        "code_challenge_method": "S256"
                    }
                    redi = redirect(target_builder.url)
                    return redi
                except ConnectTimeout:
                    return "Could not connect - check internet connection", 400
                except Exception as e:
                    return str(e), 500

            @_Listener._routes.route('/', methods=['GET', 'POST'])
            def auth_callback():
                postbox = session["postbox"]

                state = request.args.get('state', '')
                if state != postbox:
                    return """
                      <img style="max-width: 300px; height: auto; "
                        src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg"
                        alt="IHS Logo"
                      >
                      </hr>
                      <h2 style="font-family: Arial, Helvetica, sans-serif;">
                      You have another SDK session open.
                      </h2>
                    """, 403


                code = request.args.get('code')
                client_id = request.args.get('client_id')

                # exchange this code for a token
                tokens = requests.post(
                    urljoin(session["sam"], sam_urls.sam_token),
                    data={
                        "grant_type": "authorization_code",
                        "client_id": client_id,
                        "redirect_uri": localhost,
                        "code": code,
                        "code_verifier": session["code_verifier"]
                    },
                    allow_redirects=False
                )

                if tokens.status_code != 200:
                    return tokens.text, tokens.status_code

                token = tokens.json()["access_token"]
                # ok now we wanna exchange this token with catalogue
                catalogue_response = requests.post(
                    urljoin(session["catalogue"],
                            identity_urls.identity_token),
                    data={
                        "client_id": client_id,
                        "subject_token": token,
                        # "origin": "SDK"

                    },

                    allow_redirects=False
                )

                if catalogue_response.status_code != 200:
                    return catalogue_response.text, catalogue_response.status_code


                jwt = catalogue_response.json()["access_token"]
                _Listener._condition.acquire()
                _Listener.values[postbox] = jwt
                _Listener._condition.notify_all()
                _Listener._condition.release()

                logging.info("Acquired Catalogue JWT")
                return """
                  <img style="max-width: 300px; height: auto; "
                    src="https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg" 
                    alt="IHS Logo"
                  >
                  </hr>
                  <h2 style="font-family: Arial, Helvetica, sans-serif;">
                  You're now logged in. Please close this window.
                  </h2>
                """

            @_Listener._routes.route('/shutdown', methods=['GET', 'POST'])
            def shutdown():
                try:
                    pass
                    # print("shutdown")
                finally:
                    return 'Server shutting down...'

            app.register_blueprint(_Listener._routes)

            if not debug:
                try:
                    t = threading.Thread(
                        target=lambda: app.run(port=port)
                    )
                    t.daemon = False
                    t.start()
                except OSError:
                    print("Already running")

        return str(postbox)
