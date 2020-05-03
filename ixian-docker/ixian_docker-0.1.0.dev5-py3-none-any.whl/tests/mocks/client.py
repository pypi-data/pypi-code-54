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

import base64
import datetime
import json
from collections import defaultdict

import docker
import pytest
from unittest import mock

from dateutil.tz import tzlocal

from ixian.config import CONFIG
from ixian.module import load_module
from ixian_docker.modules.docker.utils.client import (
    DOCKER_REGISTRIES,
    DockerClient,
    ECRDockerClient,
)
from ixian_docker.modules.docker.utils.images import build_image
from ixian_docker.tests import event_streams


TEST_IMAGE_NAME = "ixian_docker.test"
MOCK_REGISTRY_CONFIGS = {
    "docker.io": {
        "client": DockerClient,
        "options": {"username": "tester", "password": "secret"},
    },
    "MOCK_DEFAULT_REGISTRY": {
        "client": DockerClient,
        "options": {"username": "tester", "password": "secret"},
    },
    "MOCK_DEFAULT_REGISTRY_WITH_OPTIONS": {
        "client": DockerClient,
        "options": {"foo": "bar"},
    },
    "MOCK_ECR_REGISTRY": {"client": ECRDockerClient,},
}


@pytest.fixture
def mock_docker_registries():
    CONFIG.DOCKER.REGISTRIES = MOCK_REGISTRY_CONFIGS
    yield

    # Clean docker registry - This assumes tests are running in a container and that it's safe to
    # remove docker objects after the test is complete.
    # clean_volumes
    # clean_containers
    # clean_images
    for client in DOCKER_REGISTRIES.values():
        try:
            del client.__dict__["client"]
        except KeyError:
            pass
        try:
            del client.__dict__["ecr_client"]
        except KeyError:
            pass

    DOCKER_REGISTRIES.clear()
    CONFIG.DOCKER.REGISTRIES = {}


@pytest.fixture
def mock_docker_environment(mock_environment, mock_docker_registries):
    """
    Mock the docker environment for tests:
    - docker client partially mocked:
        - local methods not mocked
        - server interactions mocked:
            - pull
            - push
    - containers, images, volumes dropped when fixture exits
    :return:
    """
    # mock docker remote methods
    mock_client = mock.MagicMock()

    # mock image get
    mock_client.images.get.return_value = True

    # mock pull/push
    mock_client.api.pull.return_value = (
        event for event in event_streams.PULL_SUCCESSFUL
    )
    mock_client.api.push.return_value = (
        event for event in event_streams.PUSH_SUCCESSFUL
    )

    # Mock login
    mock_client.login = mock.Mock()

    # Patch
    patcher = mock.patch("ixian_docker.modules.docker.utils.client.docker")
    mock_docker = patcher.start()
    mock_docker.from_env.return_value = mock_client
    yield mock_client
    patcher.stop()


def mock_build_image_if_needed():
    """
    It's difficult to partially mock the docker client so mock build_image_if_needed instead. This
    method requires build not be mocked, but that get_image methods are mocked. It would be
    preferable to mock it at a low level, but much much easier to mock build_image_if_needed.

    This mock provides an assertion method for validating calls. This helps ensure that tests using
    this mock still conform to the signature expected by build_image_if_needed
    """
    # TODO, high level mocks instead

    # Patch
    patcher = mock.patch("ixian_docker.modules.docker.utils.client.docker")
    mock_docker = patcher.start()
    mock_docker.from_env.return_value = mock_client
    yield mock_client
    patcher.stop()


# Mock base64 encoded token
MOCK_ECR_AUTHENTICATION_TOKEN = {
    "authorizationData": [
        {
            "authorizationToken": base64.b64encode(b"AWS:FAKE_AUTH_TOKEN"),
            "expiresAt": datetime.datetime(
                2019, 12, 1, 3, 32, 33, 000000, tzinfo=tzlocal()
            ),
            "proxyEndpoint": "https://FAKE_REGISTRY.dkr.ecr.us-west-2.amazonaws.com",
        }
    ],
    "ResponseMetadata": {
        "RequestId": "604fff98-520e-4b1e-99a4-c3c6dff7dffb",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "604fff98-520e-4b1e-99a4-c3c6dff7dffb",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "2709",
        },
        "RetryAttempts": 0,
    },
}


@pytest.fixture
def mock_ecr():
    patcher = mock.patch("ixian_docker.modules.docker.utils.client.boto3")
    mock_boto = patcher.start()
    mock_boto.client().get_authorization_token.return_value = (
        MOCK_ECR_AUTHENTICATION_TOKEN
    )
    yield mock_boto
    patcher.stop()
