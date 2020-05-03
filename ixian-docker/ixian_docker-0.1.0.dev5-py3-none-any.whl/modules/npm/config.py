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


class NPMConfig(Config):
    @classproperty
    def MODULE_DIR(cls):
        """Directory where ixian_docker.npm is installed"""
        from ixian_docker.modules import npm

        return os.path.dirname(os.path.realpath(npm.__file__))

    # file name for NPM config
    PACKAGE_JSON = "package.json"

    # Directory in container where node_modules is located.
    NODE_MODULES_DIR = "{DOCKER.APP_DIR}/node_modules"
    BIN = "{NPM.NODE_MODULES_DIR}/.bin"

    DOCKERFILE = "Dockerfile.npm"
    IMAGE_FILES = ["{PWD}/root/srv/etc/npm/"]

    REPOSITORY = "{DOCKER.REPOSITORY}"
    IMAGE_TAG = "npm-{TASKS.BUILD_NPM_IMAGE.HASH}"
    IMAGE = "{NPM.REPOSITORY}:{NPM.IMAGE_TAG}"

    VOLUME = "{NPM.IMAGE_TAG}"
