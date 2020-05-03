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

OPTIONS = {
    "name": "PYTHON",
    "tasks": "ixian_docker.modules.python.tasks",
    "config": "ixian_docker.modules.python.config.PythonConfig",
    "dockerfile_template": "{PYTHON.MODULE_DIR}/Dockerfile.template",
    # Dev volumes mounted only in local environment
    "dev_volumes": [
        # Pipenv
        "{PYTHON.VIRTUAL_ENV_VOLUME}:{PYTHON.VIRTUAL_ENV_DIR}",
        # Mount Pipfile in because it can't be symlinked.
        "{PWD}/Pipfile:{DOCKER.APP_DIR}/Pipfile",
        # ipython history
        "{BUILDER}/.ipython/:{DOCKER.HOME_DIR}/.ipython/",
    ],
}
