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


BLACK_DEPENDS = ["compose_runtime"]


class LintPython(VirtualTarget):
    """Virtual target for testing javascript"""

    name = "lint_py"
    parent = "lint"
    category = "testing"
    short_description = "Run all python linting tasks"


class Black(Task):
    """
    Black python formatter.

    This task is a proxy to the Black python formatter. It uses `compose`
    to execute jest within the context of the app container.

    Other arguments and flags are passed through to black.

    For Black help type: ix black --help
    """

    name = "black"
    category = "testing"
    depends = BLACK_DEPENDS
    short_description = "Black python formatter."

    def execute(self, *args):
        args = args or CONFIG.BLACK.ARGS
        return run("black", args)


class BlackCheck(Task):
    """
    Verify python code has been formatted with Black
    """

    name = "black_check"
    category = "testing"
    parent = ["lint", "lint_py"]
    depends = BLACK_DEPENDS
    short_description = "Black lint check."

    def execute(self, *args):
        args = args or CONFIG.BLACK.ARGS
        return run("black", ["--check", *args])
