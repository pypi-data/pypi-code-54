
import codecs
import pathlib
import re
import shutil
import structlog
import subprocess

import docker

from .env import get_env


logger = structlog.get_logger(__name__)


class App:
    """
    Application

    This class represents an application.
    """

    def __init__(self, name=None, root=None):
        self._name = name
        self._root = pathlib.Path(root) if root else None
        self.platform = "aws"
        self.runtime = "python3.8"
        self.version = "0.1.0"
        self._envs = {}

    @property
    def name(self):
        return self._name

    @property
    def root(self):
        return self._root

    @property
    def config(self):
        return self.root.joinpath(".cuta")

    @property
    def tag(self):
        return f"{self.name}:{self.version}"

    @property
    def base(self):
        return f"ylathouris/cuta:{self.platform}-{self.runtime}"

    def init(self):
        """
        Initialize

        Initialize new application using the current working
        directory. This method will create the required package
        files for the app.
        """
        self._root = self._root or pathlib.Path.cwd()
        self._name = self._name or self.root.name

        logger.info(f"App Context", platform=self.platform, runtime=self.runtime)
        for output in self.create_package():
            yield output

        self.create_dockerfile()

    def create_package(self):
        """
        Create package
        """
        path = self.config.joinpath("pyproject.toml")
        if path.exists():
            return

        with self.env() as env:
            logger.debug(f"Creating package", root=str(self.root), name=self.name)
            cmd = ["poetry", "init", f"--no-interaction", f"--name={self.name}"]
            exit_code, output = env.exec(cmd, stream=True)
            for chunk in output:
                yield chunk.decode("utf-8").strip()

            logger.debug(f"Locking package")
            env.exec(["poetry", "lock"])

    def create_dockerfile(self):
        """
        Create dockerfile
        """
        root = pathlib.Path(__file__).parent.parent
        template = root.joinpath("template", "Dockerfile")
        dockerfile = self.config.joinpath("Dockerfile")
        logger.debug(f"Copying Docker template")
        shutil.copyfile(template, dockerfile)

    def add(self, deps, dev=False):
        """
        Add dependencies

        Add dependencies required by the app. If `dev=True`, the
        dependencies will be added as development only dependencies
        and will not be present in the final build.
        """
        logger.info("Adding dependencies", dev=dev, deps=deps)
        with self.env() as env:
            cmd = ["poetry", "add", *deps]
            if dev:
                cmd.insert(2, "--dev")

            exit_code, output = env.exec(cmd, stream=True)
            for chunk in output:
                chunk = chunk.decode("utf-8")
                for line in chunk.splitlines():
                    yield line

    def remove(self, deps, dev=False):
        """
        Remove dependencies

        Remove dependencies required by the app.
        """
        logger.info("Removing dependencies", dev=dev, deps=deps)
        with self.env() as env:
            cmd = ["poetry", "remove", *deps]
            if dev:
                cmd.insert(2, "--dev")

            exit_code, output = env.exec(cmd, stream=True)
            for chunk in output:
                yield chunk.decode("utf-8").strip()

    def env(self):
        tag = f"ylathouris/cuta:{self.platform}-{self.runtime}"
        env = get_env(tag)
        env.workdir = f"/home/cuta/{self.name}/.cuta/"
        env.mount(self.root, f"/home/cuta/{self.name}")
        return env

    def build(self):
        """
        """
        dockerdir = self.root.joinpath(".cuta")
        client = docker.from_env()
        for output in client.api.build(tag=self.tag, path=str(dockerdir)):
            output = output.decode("utf-8")
            output = output.strip()
            output = codecs.decode(output, "unicode_escape")
            match = re.search(r":\"(.*)\S?", output, re.M)
            if match:
                yield match.group(1)
            else:
                yield repr(output)

    def shell(self):
        """
        """
        subprocess.run([
            "docker",
            "run",
            "--interactive",
            "--tty",
            "--rm",
            self.tag,
            "bash"
        ])

    def delete(self):
        """
        """
        if self.config.exists():
            logger.info(f"Deleting cuta config", path=str(self.config))
            shutil.rmtree(str(self.config))

        try:
            logger.debug(f"Removing build", tag=self.tag)
            client = docker.from_env()
            client.images.remove(self.tag, force=True)
        except docker.errors.ImageNotFound as err:
            pass
