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
import logging

import boto3
import docker

from ixian.config import CONFIG
from ixian.utils.decorators import cached_property


logger = logging.getLogger(__name__)


# Global cache of registries that are created.
DOCKER_REGISTRIES = {}


def docker_client():
    return docker.from_env()


class UnknownRegistry(Exception):
    """Exception raised when registry is not configured"""

    pass


class DockerClient:
    def __init__(self, registry, **options):
        self.registry = registry
        self.options = options

    @classmethod
    def for_registry(cls, registry):
        try:
            return DOCKER_REGISTRIES[registry]
        except KeyError:
            pass

        # Instantiate client for registry
        try:
            config = CONFIG.DOCKER.REGISTRIES[registry]
        except KeyError:
            logger.warn(f"Registry missing from DOCKER.REGISTRIES: {registry}")
            raise UnknownRegistry(registry)

        Client = config["client"]
        instance = Client(registry, **config.get("options", {}))
        DOCKER_REGISTRIES[registry] = instance

        return instance

    @cached_property
    def client(self):
        return docker_client()

    def login(self):
        # authenticate
        username = self.options.get("username", None)
        password = self.options.get("password", None)
        if not username:
            raise KeyError(
                f"Cannot login to {self.registry}, username not found in options."
            )
        if not password:
            raise KeyError(
                f"Cannot login to {self.registry}, password not found in options."
            )

        self.client.login(username, password, "", registry=self.registry)


class ECRDockerClient(DockerClient):
    @cached_property
    def ecr_client(self):
        kwargs = dict(region_name="us-west-2")
        kwargs.update(self.options)
        return boto3.client("ecr", **kwargs)

    def login(self):
        # fetch credentials from ECR
        logger.debug(
            "Authenticating with ECR: {}".format(
                self.options.get("region_name", "us-west-2")
            )
        )
        token = self.ecr_client.get_authorization_token()
        username, password = (
            base64.b64decode(token["authorizationData"][0]["authorizationToken"])
            .decode()
            .split(":")
        )
        registry = token["authorizationData"][0]["proxyEndpoint"]

        # authenticate
        self.client.login(username, password, "", registry=registry)
