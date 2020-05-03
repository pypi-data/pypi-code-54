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

import json
import logging
from collections import defaultdict

from docker.errors import NotFound as DockerNotFound
from docker.errors import ImageNotFound as ImageNotFound

from ixian.module import MODULES
from ixian.utils.filesystem import pwd
from ixian.utils.process import execute
from ixian.config import CONFIG
from ixian_docker.modules.docker.utils.client import (
    DockerClient,
    UnknownRegistry,
    docker_client,
)
from ixian_docker.modules.docker.utils.print import (
    print_docker_transfer_events,
    format_pull_status_minimal,
)
from ixian_docker.utils.net import is_valid_hostname


logger = logging.getLogger(__name__)


def image_exists(name):
    """
    Check if image exists locally.
    :param name: name of image.
    :return: True/False
    """
    client = docker_client()
    try:
        client.images.get(name)
    except DockerNotFound:
        return False
    else:
        return True


def image_exists_in_registry(repository, tag=None):
    """
    Check if image exists in the registry.
    :param name: name of image.
    :return: True/False
    """
    # Disable check till ECR Client works
    registry = parse_registry(repository)
    client = DockerClient.for_registry(registry)
    client.login()
    image = f"{repository}:{tag or 'latest'}"
    logger.debug(f"Checking registry for {image}")
    try:
        client.client.images.get_registry_data(image)
    except DockerNotFound:
        return False
    return True


def delete_image(name, force=False):
    client = docker_client()
    try:
        image = client.images.get(name)
    except ImageNotFound:
        return False
    client.images.remove(image.id, force=force)
    return True


EMPTY_LINE = b'{"stream":"\\n"}'


def build_image(dockerfile, tag, context=None, **kwargs):
    """Build a docker image.

    Builds a docker image. This is a shim around Docker-py that adds some
    ixian utilities to it.

    :param tag: Tag for image.
    :param file: Dockerfile.
    :param context: build context, default is the working directory.
    :param args: args to pass as build-args to build
    """
    if not context:
        context = pwd()
    logger.debug(f"Building image dockerfile={dockerfile} tag={tag} context={context}")

    client = docker_client()

    stream = client.api.build(path=context, dockerfile=dockerfile, tag=tag, **kwargs)
    seen_layers = defaultdict(set)

    # log output from build
    buffer = bytearray()
    for message in stream:

        # Add message to buffer and then split it on CRs to find individual lines. Messages may not
        # include a complete line (often because they are too large). Consume only the complete
        # lines.
        buffer.extend(message)
        split_lines = buffer.split(b"\r\n")
        if buffer.endswith(b"\r\n"):
            # ends in complete line, consume all lines
            buffer.clear()
            last_line = len(split_lines)
        else:
            # ends in partial line, only consume complete lines
            buffer = split_lines[-1]
            last_line = len(split_lines) - 1

        for line in split_lines[:last_line]:

            if not line or line == EMPTY_LINE:
                continue

            try:
                decoded_line = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                logger.error("COULDN'T DECODE STREAM")
                logger.error(f"Error: {e}")
                logger.error(f"line={line}")
                decoded_line = {}

            # build steps
            if "stream" in decoded_line:
                logger.info(decoded_line["stream"].rstrip("\\n").rstrip("\n"))

            # errors
            elif "errorDetail" in decoded_line:
                logger.error(decoded_line["errorDetail"]["message"])
                # TODO: raise this error somehow, should reach cli

            # base image pull status
            elif "status" in decoded_line:
                status = decoded_line["status"]
                logger.info(format_pull_status_minimal(status, seen_layers))


def build_image_if_needed(
    repository,
    tag=None,
    dockerfile="Dockerfile",
    context=None,
    pull=True,
    recheck=None,
    force=False,
    **kwargs,
):
    # if local: skip
    # if remote: pull & skip
    # else: build
    image_and_tag = "{}:{}".format(repository, tag or "latest")

    logger.debug(f"Attempting to build {image_and_tag}")

    if not force:
        if image_exists(image_and_tag):
            logger.debug("Image exists, skipping build.")
            return
        else:
            logger.debug("Image does not exist.".format(tag))

        try:
            if pull and image_exists_in_registry(repository, tag):
                logger.debug("Image exists on registry. Pulling image.")
                try:
                    pull_image(repository, tag)
                except DockerNotFound:
                    logger.debug("Image could not be pulled: NotFound")
                    pass
                else:
                    logger.debug("Image pulled.")
                    # Re-check, if task now passes then build can be skipped
                    if not recheck or recheck():
                        logger.debug("Check passed, skipping build.")
                        # TODO: get image and return
                        return
            elif pull:
                logger.debug("Image does not exist on registry.")
        except UnknownRegistry as exception:
            logger.warn(
                f"Registry '{str(exception)}' is not configured, couldn't check for remote image."
            )

    return build_image(dockerfile, image_and_tag, context=context, **kwargs)


def parse_registry(repository):
    """
    Parse hostname from repository (image name)
    :param repository: image name, which may or may not include hostname
    :return: hostname of registry
    """

    # the repository hostname can only be before the slash. So trim it off because it confuses the
    # netloc parsing method below.
    hostname = repository.split("/")[0]

    # Use the hostname if it's valid, otherwise return the default docker registry (docker.io)
    if is_valid_hostname(hostname):
        return hostname
    else:
        return "docker.io"


def pull_image(repository, tag=None, silent=False):
    """
    Pull an image from a repository.

    :param repository: image to pull from. Docker hub assumed if repository does not begin with a
     hostname
    :param tag: tag of image. defaults to "latest"
    :return:
    """
    resolved_tag = tag or "latest"

    registry = parse_registry(repository)
    client = DockerClient.for_registry(registry)
    client.login()

    if not silent and tag is None:
        # TODO: logger
        print("Using default tag: latest")

    event_stream = client.client.api.pull(
        repository, resolved_tag or "latest", stream=not silent, decode=not silent
    )
    if not silent:
        print_docker_transfer_events(event_stream)

    # Print pulled image
    # TODO: logger
    print("{}:{}".format(repository, resolved_tag))


def push_image(repository, tag=None, silent=False):
    """
    Push an image to a registry.

    :param repository: repository to push to. Docker hub  assumed if repository does not begin
     with a hostname
    :param tag: image tag to push
    :param silent: don't output progress, default is False
    :return:
    """
    # default tag to latest
    resolved_tag = tag or "latest"

    registry = parse_registry(repository)
    client = DockerClient.for_registry(registry)
    client.login()

    event_stream = client.client.api.push(
        repository, resolved_tag or "latest", stream=not silent, decode=not silent
    )
    if not silent:
        print_docker_transfer_events(event_stream)
