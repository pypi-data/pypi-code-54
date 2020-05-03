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

from ixian.build import write_file
from ixian.task import Task
from ixian.config import CONFIG
from ixian.modules.filesystem.file_hash import FileHash
from ixian_docker.modules.docker.checker import DockerImageExists
from ixian_docker.modules.docker.tasks import run
from ixian_docker.modules.docker.utils.dockerfile import build_dockerfile
from ixian_docker.modules.docker.utils.images import build_image_if_needed
from ixian_docker.modules.docker.utils.volumes import delete_volume


class BuildWebpackImage(Task):
    """
    Build image with javascript, css, etc. compiled by Webpack.
    """

    name = "build_webpack_image"
    parent = "build_image"
    depends = ["build_npm_image"]
    category = "build"
    short_description = "Build Webpack image"
    check = [
        FileHash("{WEBPACK.DOCKERFILE}", *CONFIG.resolve("WEBPACK.IMAGE_FILES")),
        DockerImageExists("{WEBPACK.IMAGE}"),
    ]

    @property
    def __check(self):
        checks = {
            "config": FileHash("{WEBPACK.DOCKERFILE}"),
            "src": CONFIG.resolve("WEBPACK.IMAGE_FILES"),
            "image": DockerImageExists("{WEBPACK.IMAGE}"),
        }

        if CONFIG.ENV == "dev":
            checks["volume"] = FileHashCompare("src", "{WEBPACK.VOLUME_HOST_PATH}")
        return checks

    def execute(self, pull=True):
        print("CONFIG.WEBPACK.DOCKERFILE: ", CONFIG.WEBPACK.DOCKERFILE)
        if CONFIG.WEBPACK.DOCKERFILE.endswith(".jinja"):
            print("writing dockerfile?: ", CONFIG.WEBPACK.RENDERED_DOCKERFILE)
            dockerfile = CONFIG.WEBPACK.RENDERED_DOCKERFILE
            write_file(dockerfile, build_dockerfile(CONFIG.WEBPACK.DOCKERFILE))

        else:
            dockerfile = CONFIG.WEBPACK.DOCKERFILE
        print("dockerfile: ", dockerfile)
        build_image_if_needed(
            repository=CONFIG.WEBPACK.REPOSITORY,
            tag=CONFIG.WEBPACK.IMAGE_TAG,
            dockerfile=dockerfile,
            force=self.__task__.force,
            pull=pull,
            # recheck=self.check.check,
            buildargs={
                "FROM_REPOSITORY": CONFIG.DOCKER.REPOSITORY,
                "FROM_TAG": CONFIG.NPM.IMAGE_TAG,
            },
        )


def clean_webpack_volume():
    delete_volume(CONFIG.WEBPACK.COMPILED_STATIC_VOLUME)
    delete_volume(CONFIG.WEBPACK.CACHE_LOADER_VOLUME)


class WebpackVolume(Task):
    """
    Builds development volume with webpack

    This task runs the webpack compiler. It runs using `compose` to run within
    the context of the app image.
    """

    name = "webpack_volume"
    category = "build"
    clean = clean_webpack_volume
    depends = ["compose_runtime"]
    short_description = "Build webpack development volume"

    def execute(self):
        # 1. get hash of source
        image_exists = False
        volume_exists = False

        if image_exists:
            pass
            # - Mount Image
            # - Copy files from mount
        elif volume_exists:
            pass
            # setup volume as current
        else:
            pass
            # create directory
            # build with webpack


class Webpack(Task):
    """
    Run webpack javascript/css compiler.

    This task runs the webpack compiler. It runs using `compose` to run within
    the context of the app image.
    """

    name = "webpack"
    category = "build"
    clean = clean_webpack_volume
    depends = ["compose_runtime"]
    short_description = "Webpack javascript/css compiler"
    config = [
        "{WEBPACK.CONFIG_FILE}",
        "{WEBPACK.CONFIG_FILE_PATH}",
        "{WEBPACK.COMPILED_STATIC_DIR}",
        "{WEBPACK.COMPILED_STATIC_VOLUME}",
        "{WEBPACK.ARGS}",
    ]

    def execute(self, *args):
        # compiled_args = list(CONFIG.WEBPACK.ARGS) + list(args)
        return run("./node_modules/.bin/webpack", *CONFIG.WEBPACK.ARGS, *args)
