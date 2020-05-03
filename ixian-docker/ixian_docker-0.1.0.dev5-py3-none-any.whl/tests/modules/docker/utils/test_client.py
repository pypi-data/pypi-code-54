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

from unittest import mock

import pytest
import docker

from ixian_docker.modules.docker.utils.client import (
    DockerClient,
    docker_client,
    UnknownRegistry,
)


def test_get_client():
    """Sanity check"""
    assert isinstance(docker_client(), docker.DockerClient)


class TestDockerClient:
    def test_for_registry(self, mock_docker_environment):
        mock_client = mock_docker_environment
        client = DockerClient.for_registry("MOCK_DEFAULT_REGISTRY")
        assert isinstance(client, DockerClient)
        assert client.client is mock_client

        # sanity test mocks
        client.client.api.push.assert_not_called()
        client.client.api.pull.assert_not_called()
        client.client.login.assert_not_called()

    def test_unknown_registry(self, mock_docker_environment):
        """Test requesting a registry that isn't configured"""
        with pytest.raises(UnknownRegistry):
            DockerClient.for_registry("REGISTRY_DOES_NOT_EXIST")

    def test_client_options(self, mock_docker_environment):
        mock_client = mock_docker_environment
        client = DockerClient.for_registry("MOCK_DEFAULT_REGISTRY")
        assert isinstance(client, DockerClient)
        assert client.client is mock_client

    def test_login(self, mock_docker_environment):
        client = DockerClient.for_registry("MOCK_DEFAULT_REGISTRY")
        client.login()
        client.client.login.assert_called_with(
            "tester", "secret", "", registry="MOCK_DEFAULT_REGISTRY"
        )

    def test_login_without_username(self, mock_docker_environment):
        client = DockerClient.for_registry("MOCK_DEFAULT_REGISTRY")
        client.options.pop("username", None)
        with pytest.raises(KeyError):
            client.login()

    def test_login_without_password(self, mock_docker_environment):
        client = DockerClient.for_registry("MOCK_DEFAULT_REGISTRY")
        client.options.pop("password", None)
        with pytest.raises(KeyError):
            client.login()


class TestECRDockerClient:
    def test_for_registry(self, mock_docker_environment, mock_ecr):
        mock_client = mock_docker_environment
        client = DockerClient.for_registry("MOCK_ECR_REGISTRY")
        assert isinstance(client, DockerClient)
        assert client.client is mock_client

        # sanity test mocks
        client.client.api.push.assert_not_called()
        client.client.api.pull.assert_not_called()
        client.client.login.assert_not_called()

        # get ecr_client
        assert isinstance(client.ecr_client, mock.Mock)

    def test_login(self, mock_docker_environment, mock_ecr):
        client = DockerClient.for_registry("MOCK_ECR_REGISTRY")
        client.login()
        client.client.login.assert_called_with(
            "AWS",
            "FAKE_AUTH_TOKEN",
            "",
            registry="https://FAKE_REGISTRY.dkr.ecr.us-west-2.amazonaws.com",
        )
