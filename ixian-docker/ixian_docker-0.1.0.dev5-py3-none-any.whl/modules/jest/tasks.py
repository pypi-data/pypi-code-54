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

from ixian.config import CONFIG
from ixian.task import Task, VirtualTarget
from ixian_docker.modules.docker.tasks import run


JEST_DEPENDS = ["compose_runtime"]


class TestJS(VirtualTarget):
    """Virtual target for testing javascript"""

    name = "test_js"
    category = "testing"
    short_description = "Run all javascript testing tasks"


class Jest(Task):
    """
    Jest javascript test runner.

    This task is a proxy to the Jest javascript test runner. It uses `compose`
    to execute jest within the context of the app container.

    Configuration is configured by default as:
        --config={JEST.CONFIG_FILE_PATH}

    Other arguments and flags are passed through to jest.

    For Jest help type: ix jest --help
    """

    name = "jest"
    category = "testing"
    depends = JEST_DEPENDS
    parent = ["test", "test_js"]
    short_description = "Jest javascript test runner."

    def execute(self, *args):
        command = CONFIG.format("{JEST.BIN} --config={JEST.CONFIG_FILE_PATH}")
        return run(command, args)
