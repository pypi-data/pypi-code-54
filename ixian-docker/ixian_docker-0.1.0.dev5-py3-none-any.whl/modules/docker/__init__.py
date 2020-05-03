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
    "name": "DOCKER",
    "tasks": "ixian_docker.modules.docker.tasks",
    "config": "ixian_docker.modules.docker.config.DockerConfig",
    # Dev volumes mounted only in local environment
    "dev_volumes": [
        "{PWD}:{DOCKER.PROJECT_DIR}",
        "{BUILDER}/.bash_history:{DOCKER.HOME_DIR}/.bash_history",
        "{PWD}/bin/:{DOCKER.APP_DIR}/bin",
        "{PWD}/.env:{DOCKER.APP_DIR}/.env",
    ],
}
