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
from ixian.task import Task
from ixian_docker.modules.docker.tasks import run


PYTEST_DEPENDS = ["compose_runtime"]


class Pytest(Task):
    """
    Pytest python test runner.

    This task is a proxy to the Pytest python test runner. It uses `compose`
    to execute Pytest within the context of the app container.

    Other arguments and flags are passed through to Pytest.

    For Pytest help type: ix pytest --help
    """

    name = "pytest"
    category = "testing"
    depends = PYTEST_DEPENDS
    short_description = "Pytest test runner."

    def execute(self, *args):
        args = [*CONFIG.PYTEST.ARGS, *args]
        print("args: ", args)
        return run("pytest", args)
