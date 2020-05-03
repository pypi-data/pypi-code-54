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

from ixian.check.checker import hash_object
from ixian.config import Config, CONFIG
from ixian.modules.filesystem.file_hash import FileHash
from ixian.utils.decorators import classproperty


class BowerConfig(Config):
    @classproperty
    def MODULE_DIR(cls):
        """Directory where ixian_docker.webpack is installed"""
        from ixian_docker.modules import bower

        return os.path.dirname(os.path.realpath(bower.__file__))

    # Directory path and volume for bower_components (installed files)
    COMPONENTS_DIR = "{DOCKER.APP_DIR}/bower_components"
    COMPONENTS_VOLUME = "{PROJECT_NAME}.bower_components"

    # Config file and path
    CONFIG_FILE = "bower.json"
    CONFIG_FILE_PATH = "{DOCKER.PROJECT_DIR}/{BOWER.CONFIG_FILE}"

    # Path to bower executable
    BIN = "{NPM.NODE_MODULES_DIR}/.bin/bower"

    # Default args included in every call to bower
    ARGS = ["--config.interactive=false", "--allow-root"]

    DOCKERFILE = "Dockerfile.bower"
    IMAGE_FILES = ["{PWD}/root/srv/etc/bower/"]

    REPOSITORY = "{DOCKER.REPOSITORY}"
    IMAGE_TAG = "bower-{TASKS.BUILD_BOWER_IMAGE.HASH}"
    IMAGE = "{BOWER.REPOSITORY}:{BOWER.IMAGE_TAG}"
