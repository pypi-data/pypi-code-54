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


PRETTIER_DEPENDS = ["compose_runtime"]


class LintJS(VirtualTarget):
    """Virtual target for linting javascript"""

    name = "lint_js"
    parent = "lint"
    category = "testing"
    short_description = "Run all javascript linting tasks"


class Prettier(Task):
    """
    Prettier javascript formatter.

    This task is a proxy to the Prettier python formatter. It uses `compose`
    to execute prettier within the context of the app container.

    Other arguments and flags are passed through to prettier.

    For Prettier help type: ix prettier --help
    """

    name = "prettier"
    category = "testing"
    depends = PRETTIER_DEPENDS
    short_description = "Black python formatter."

    def execute(self, *args):
        args = args or [
            "--write",
            "--list-different",
            "--color",
            "{PRETTIER.SRC}/**/*.js",
        ]
        return run("{PRETTIER.BIN}", args)


class PrettierCheck(Task):
    """
    Verify javascript code has been formatted with Prettier
    """

    name = "prettier_check"
    category = "testing"
    parent = ["lint", "lint_js"]
    depends = PRETTIER_DEPENDS
    short_description = "Prettier javascript lint check."

    def execute(self, *args):
        args = args or [
            "--check",
            "--color",
            "{PRETTIER.SRC}/**/*.js",
        ]
        return run("{PRETTIER.BIN}", args)
