# Copyright [2018-2020] Peter Krenesky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ixian.config import Config
from ixian.utils.decorators import classproperty


class DjangoConfig(Config):
    @classproperty
    def MODULE_DIR(cls):
        """Directory where ixian_docker.python is installed"""
        from ixian_docker.modules import django

        return os.path.dirname(os.path.realpath(django.__file__))

    # Directory containing django settings
    SETTINGS_DIR = "{PYTHON.ROOT_MODULE}/settings"

    # Module containing settings
    SETTINGS_MODULE = "{PYTHON.ROOT_MODULE}.settings"

    # default settings
    SETTINGS_FILE = "{DJANGO.SETTINGS_MODULE}.base"

    # settings file for tests
    SETTINGS_TEST = "{DJANGO.SETTINGS_MODULE}.test"

    # Path to UWSGI configuration file on host.
    UWSGI_INI = "uwsgi.ini"

    # Host for Compose. 0.0.0.0 should be used for docker default network
    # config.
    HOST = "0.0.0.0"

    # Port to expose for both Compose and Docker run.
    PORT = "8000"


DJANGO_CONFIG = DjangoConfig()
