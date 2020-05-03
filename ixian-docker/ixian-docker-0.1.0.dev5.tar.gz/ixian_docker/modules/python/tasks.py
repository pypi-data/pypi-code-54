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

import docker
import pip

from ixian.config import CONFIG
from ixian.modules.filesystem.file_hash import FileHash
from ixian.task import Task, VirtualTarget
from ixian.utils.process import execute
from ixian_docker.modules.docker.checker import (
    DockerVolumeExists,
    DockerImageExists,
)
from ixian_docker.modules.docker.tasks import run
from ixian_docker.modules.docker.utils.client import docker_client
from ixian_docker.modules.docker.utils.images import build_image_if_needed
from ixian.runner import ExitCodes

PYTHON_DEPENDS = ["build_base_image"]


def python_local_package_mount_flags():
    return []


class BuildPythonImage(Task):

    name = "build_python_image"
    parent = ["build_image", "compose_runtime"]
    depends = ["build_base_image"]
    category = "build"
    short_description = "Build Python image"
    check = [
        FileHash("{PYTHON.DOCKERFILE}", *CONFIG.resolve("PYTHON.IMAGE_FILES")),
        DockerImageExists("{PYTHON.IMAGE}"),
    ]

    def execute(self, pull=True):
        build_image_if_needed(
            repository=CONFIG.PYTHON.REPOSITORY,
            tag=CONFIG.PYTHON.IMAGE_TAG,
            dockerfile=CONFIG.PYTHON.DOCKERFILE,
            force=self.__task__.force,
            pull=pull,
            # recheck=self.check.check,
            buildargs={
                "FROM_REPOSITORY": CONFIG.DOCKER.REPOSITORY,
                "FROM_TAG": CONFIG.DOCKER.BASE_IMAGE_TAG,
            },
        )


class CreatePyEnv(Task):
    name = "create_pyenv"
    category = "python"
    contexts = ["container"]
    short_description = "Creates a python pyenv."
    checks = []
    parent = "build_platform"

    def execute(self):
        commands = [
            " ".join(["install_clean"] + CONFIG.PYTHON.APT_PACKAGES),
            "curl https://pyenv.run | bash",
        ]

        for command in commands:
            execute(command)

        pyenv_shell("pyenv install {PYTHON.VERSION}")


def pyenv_shell(command):
    init = 'eval "$(pyenv init -)" && '
    venv_init = 'eval "$(pyenv virtualenv-init -)"'
    execute(f"{init} && {venv_init} && {command}")


class InstallPythonPackages(Task):
    name = "install_python_packages"
    category = "python"
    contexts = ["container"]
    short_description = "Installs python packages into a virtual environment."
    check = [
        FileHash("{PYTHON.DOCKERFILE}", *CONFIG.resolve("PYTHON.IMAGE_FILES")),
        DockerImageExists("{PYTHON.IMAGE}"),
    ]
    depends = "create_pyenv"

    def execute(self):
        cmd = " ".join(["pip install"] + CONFIG.PYTHON.REQUIREMENTS_FILES)
        execute(cmd)


class TestPython(VirtualTarget):
    """Virtual target for python tests"""

    name = "test_py"
    category = "testing"
    short_description = "Run all python test tasks"


class Pip(Task):
    """
    Pip package manager
    """

    name = "pip"
    category = "libraries"
    depends = PYTHON_DEPENDS
    short_description = "Pip python package manager"

    def execute(self, *args):
        return run("pip", *args)
