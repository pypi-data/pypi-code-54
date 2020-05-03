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

import pytest

from ixian.config import CONFIG


EXPECTED_FIELDS = [
    "APP_BIN",
    "APP_DIR",
    "BASE_IMAGE",
    "BASE_IMAGE_FILES",
    "BASE_IMAGE_TAG",
    "COMPOSE_FLAGS",
    "DEFAULT_APP",
    "DEV_VOLUMES",
    "DEV_ENV",
    "DOCKERFILE",
    "DOCKERFILE_BASE",
    "DOCKERFILE_TEMPLATE",
    "ENV",
    "ENV_DIR",
    "HOME_DIR",
    "IMAGE",
    "IMAGE_TAG",
    "MODULE_CONTEXT",
    "MODULE_DIR",
    "PROJECT_DIR",
    "REGISTRY",
    "REGISTRY_PATH",
    "REPOSITORY",
    "ROOT_MODULE_DIR",
    "VOLUMES",
]


class TestDockerConfig:
    @pytest.mark.parametrize("field", EXPECTED_FIELDS)
    def test_read(self, field, mock_environment, snapshot):
        """
        Test reading default config values and testing property getter functions.
        """
        snapshot.assert_match(getattr(CONFIG.DOCKER, field))

    def test_task_hash(self, mock_environment, snapshot):
        snapshot.assert_match(CONFIG.TASKS.BUILD_BASE_IMAGE)
        snapshot.assert_match(CONFIG.TASKS.BUILD_IMAGE)
