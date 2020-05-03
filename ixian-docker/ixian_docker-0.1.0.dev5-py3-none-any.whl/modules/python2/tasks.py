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

from ixian.config import CONFIG
from ixian.modules.filesystem.file_hash import FileHash
from ixian.task import Task, VirtualTarget
from ixian_docker.modules.docker.checker import DockerVolumeExists
from ixian_docker.modules.docker.tasks import run
from ixian_docker.modules.docker.utils import docker_client
from ixian.runner import ERROR_TASK

PYTHON_DEPENDS = ["build_app_image"]


class TestPython(VirtualTarget):
    """Virtual target for python tests"""

    name = "test_py"
    category = "testing"
    short_description = "Run all python test tasks"


def clean_pipenv():
    """
    Remove pipenv volume
    """
    try:
        volume = docker_client().volumes.get(CONFIG.PYTHON.VIRTUAL_ENV_VOLUME)
    except docker.errors.NotFound:
        return ERROR_TASK
    else:
        volume.remove(True)


class Pipenv(Task):
    """
    Run a pipenv command.

    This runs in the builder container with volumes mounted.
    """

    name = "pipenv"
    category = "libraries"
    short_description = "PipEnv environment manager"
    depends = PYTHON_DEPENDS
    clean = clean_pipenv

    def execute(self, *args):
        return run("pipenv", *args)


class BuildPipenv(Task):
    """Run pipenv install"""

    name = "build_pipenv"
    category = "build"
    clean = clean_pipenv
    short_description = "Install python packages with pipenv"
    # parent = "build_app"
    depends = PYTHON_DEPENDS
    check = [
        FileHash("Pipfile", "Pipfile.lock",),
        DockerVolumeExists("{CONFIG.PYTHON.VIRTUAL_ENV_VOLUME}"),
    ]

    def execute(self, *args):
        pass
        # return compose('pipenv install', flags=['--dev'], *args)
