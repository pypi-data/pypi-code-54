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

import logging

import docker
from docker.errors import NotFound as DockerNotFound

from ixian.utils.process import execute
from ixian.config import CONFIG
from ixian_docker.modules.docker.utils.client import docker_client


def delete_volume(image):
    try:
        volume = docker_client().volumes.get(image)
    except docker.errors.NotFound:
        pass
    else:
        volume.remove(True)
        logger.debug("Deleted docker image: %s" % image)


def delete_all_volumes():
    raise NotImplementedError


def volume_exists(tag):
    client = docker.from_env()
    try:
        client.images.get(tag)
    except DockerNotFound:
        return False
    else:
        return True


# TODO: deprecate this and let docker-py handle formatting volumes
# def convert_volume_flags(volumes):
#    """Format volume patterns into volume flags.
#
#
#
#    :param volumes: list of volume strings
#    :return: list of volume flags
#    """
#    return ['-v %s' % CONFIG.format(volume) for volume in volumes]
