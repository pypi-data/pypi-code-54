#    Copyright 2020 Francesco Lombardo <franclombardo@gmail.com>

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

__all__ = ("PythonArango")

from functools import partial
from mimetypes import guess_type
import sys

from flask import abort, current_app, request

from arango import ArangoClient


class PythonArango(object):

    """Manages ArangoDB connections for your Flask app.
    PythonArango objects provide access to ArangoDB MongoDB server via the :attr:`db`
    attribute. You must either pass the :class:`~flask.Flask`
    app to the constructor, or call :meth:`init_app`.
    """

    def __init__(self, app=None):
        self.client = None
        self.db = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        # Initialize the client for ArangoDB.
        self.client = ArangoClient(hosts='http://localhost:8529')

        # Connect to "test" database as root user.
        self.db = self.client.db('test', username='root', password='12345678')
        print('Init_app')
        