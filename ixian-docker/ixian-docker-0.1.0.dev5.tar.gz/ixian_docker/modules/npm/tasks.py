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

import logging

from ixian.config import CONFIG
from ixian.modules.filesystem.file_hash import FileHash
from ixian.task import Task
from ixian_docker.modules.docker.checker import DockerImageExists
from ixian_docker.modules.docker.tasks import run
from ixian_docker.modules.docker.utils.images import build_image_if_needed
from ixian_docker.modules.docker.utils.volumes import delete_volume

logger = logging.getLogger(__name__)
NPM_DEPENDS = ["build_app_image"]


def remove_npm_volume():
    """
    Remove node_modules volume
    """
    delete_volume(CONFIG.NPM.NODE_MODULES_VOLUME)


class BuildNPMImage(Task):
    name = "build_npm_image"
    parent = ["build_image", "compose_runtime"]
    depends = ["build_base_image"]
    category = "build"
    short_description = "Build NPM image"
    check = [
        FileHash("{NPM.DOCKERFILE}", *CONFIG.resolve("NPM.IMAGE_FILES")),
        DockerImageExists("{NPM.IMAGE}"),
    ]

    def execute(self, pull=True):
        build_image_if_needed(
            repository=CONFIG.NPM.REPOSITORY,
            tag=CONFIG.NPM.IMAGE_TAG,
            dockerfile=CONFIG.NPM.DOCKERFILE,
            force=self.__task__.force,
            pull=pull,
            # recheck=self.check.check,
            buildargs={
                "FROM_REPOSITORY": CONFIG.DOCKER.REPOSITORY,
                "FROM_TAG": CONFIG.DOCKER.BASE_IMAGE_TAG,
            },
        )


class NCU(Task):
    """Update package.json with Node Check Update (ncu)"""

    name = "ncu"
    category = "Libraries"
    # TODO: depends without injecting it into parent task
    depends = ["compose_runtime"]
    short_description = "Update npm libraries in package.json"
    clean = remove_npm_volume

    def execute(self, *args):
        return run("ncu", args)


class NPM(Task):
    """Run npm within the context of the app container"""

    name = "npm"
    category = "Libraries"
    depends = ["compose_runtime"]
    short_description = "NPM package manager."
    clean = remove_npm_volume

    def execute(self, *args):
        args = args or ["install"]
        return run("npm", args)
