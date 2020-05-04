
import io
import os
import pathlib
import logging
import structlog
import subprocess
import tarfile

import docker


logger = structlog.get_logger(__name__)


class Environment:
    """
    Environment

    This class represents a container-based environment.
    """

    def __init__(self, image):
        self._image = image
        self._container = None
        self._volumes = {}
        self.workdir = "/home/cuta"
        self._docker = None

    @property
    def docker(self):
        if not self._docker:
            self._docker = docker.from_env()

        return self._docker

    @property
    def image(self):
        return self._image

    @property
    def container(self):
        return self._container

    @property
    def volumes(self):
        return self._volumes

    @property
    def status(self):
        return self.container.status if self.container else None

    @property
    def active(self):
        """
        Check if the environment is active.

        The environment is active when the container for it
        is running.
        """
        return self.status == "running"

    def mount(self, source, target=None, mode="rw"):
        """
        Mount source directory
        """
        target = target or "/home/cuta"
        self._volumes[source] = {"bind": target, "mode": mode}

    def unmount(self, source):
        """
        Unmount source directory
        """
        self._volumes.pop(source, None)

    def activate(self):
        """
        Activate

        Activate the environment (i.e. start container)
        """
        if self.active:
            return

        command = ["sleep", "infinity"]
        self._container = self.docker.containers.create(
            self.image,
            command=command,
            volumes=self.volumes,
            working_dir=self.workdir,
            auto_remove=True,
            )
        self._container.start()
        self._container.reload()

        logger.info(f"Environment activated", container_id=self.container.id)

    def deactivate(self):
        """
        Deactive

        Deactivate the shell (i.e. kill and remove container)
        """
        if not self.active:
            return

        container_id = self.container.id
        self.container.kill()
        self._container = None

        logger.info(f"Environment deactivated", container_id=container_id)

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, *exc_details):
        self.deactivate()

    def exec(self, cmd, **kwargs):
        """
        Execute the given command

        Execute the given command inside the container.
        """
        if not self.container:
            raise RuntimeError("Environment must be activated")

        return self.container.exec_run(cmd, **kwargs)

    def get_file(self, source, target):
        """
        Get file

        Copy source file to the given target location.
        """
        if not self.container:
            raise RuntimeError("Environment must be activated")

        # Get archive (tar) from the container.
        stream = io.BytesIO()
        chunks, stat = self.container.get_archive(str(source))
        for chunk in chunks:
            stream.write(chunk)

        # Move cursor back to the beginning of the file.
        stream.seek(0)

        # Extract file data and write it to the target.
        source = pathlib.Path(source)
        target = pathlib.Path(target)
        tar = tarfile.TarFile(fileobj=stream)
        extracted = tar.extractfile(source.name)
        with target.open("wb") as file_:
            data = extracted.read()
            file_.write(data)

        logger.info(f"Copied {self.container.id}:{source} to {target}")

        return target


def pull(name):
    """
    Pull environment from remote repository (i.e. DockerHub)
    """
    image = get_image(name)
    if not image:
        client = docker.from_env()
        output = client.api.pull(name, stream=True, decode=True)
        for item in output:
            yield item


def exists(name):
    """
    Check if the given environment exists locally
    """
    return bool(get_env(name))


def get_env(name):
    """
    Get environment with the given name/id.
    """
    image = get_image(name)
    return Environment(image) if image else None


def get_image(name):
    """
    Get docker image with the given name/id.
    """
    client = docker.from_env()
    try:
        image = client.images.get(name)
    except docker.errors.ImageNotFound as err:
        image = None

    return image
