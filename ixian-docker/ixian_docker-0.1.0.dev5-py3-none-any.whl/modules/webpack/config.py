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


class WebpackConfig(Config):
    @classproperty
    def MODULE_DIR(cls):
        """Directory where ixian_docker.webpack is installed"""
        from ixian_docker.modules import webpack

        return os.path.dirname(os.path.realpath(webpack.__file__))

    # Directory in container where compiled files are written.
    COMPILED_STATIC_DIR = "{DOCKER.APP_DIR}/compiled_static"

    # Volumes used in development
    COMPILED_STATIC_VOLUME = "{PROJECT_NAME}.compiled_static"
    CACHE_LOADER_VOLUME = "{PROJECT_NAME}.cache_loader"

    # Webpack config file and path within the container.
    CONFIG_FILE = "webpack.config.js"
    CONFIG_DIR = "{DOCKER.APP_DIR}/etc/webpack"
    CONFIG_FILE_PATH = "{WEBPACK.CONFIG_DIR}/{WEBPACK.CONFIG_FILE}"

    # Directories with sources to compile.
    SOURCE_DIRS = ["src/static"]

    # Base arguments added to all calls to `webpack`
    ARGS = [
        "--progress",
        "--colors",
        "--config {WEBPACK.CONFIG_FILE_PATH}",
        "--output-path {WEBPACK.COMPILED_STATIC_DIR}",
    ]

    DOCKERFILE = "{WEBPACK.MODULE_DIR}/Dockerfile.jinja"
    RENDERED_DOCKERFILE = "{BUILDER}/Dockerfile.webpack"
    IMAGE_FILES = ["{PWD}/root/srv/etc/webpack/"]
    BUILD_ARGS = {
        "ETC": "{WEBPACK.ETC}",
        "HOST_ETC": "{WEBPACK.HOST_ETC}",
        "SRC": "{WEBPACK.SOURCE_DIRS}",
    }

    REPOSITORY = "{DOCKER.REPOSITORY}"
    IMAGE_TAG = "webpack-{TASKS.BUILD_WEBPACK_IMAGE.HASH}"
    IMAGE = "{WEBPACK.REPOSITORY}:{WEBPACK.IMAGE_TAG}"

    BIN = "{NPM.BIN}/webpack"
    ETC = "{DOCKER.APP_DIR}/etc/webpack"
    HOST_ETC = "root{WEBPACK.ETC}"

    @classproperty
    def RUN_CMD(self):
        args = " \ \n  ".join(CONFIG.WEBPACK.ARGS)
        return f"{CONFIG.WEBPACK.BIN} {args}"


WEBPACK_CONFIG = WebpackConfig()
