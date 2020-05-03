import pytest

from ixian.config import CONFIG
from ixian.runner import run
from ixian_docker.modules.docker.utils.images import image_exists, delete_image
from ixian_docker.tests.mocks.client import MOCK_REGISTRY_CONFIGS


class TaskTests:
    def test_help(self, snapshot, mock_cli, capsys):
        """
        Tests ixian help message for task.
        """
        mock_cli.mock_in(f"help {self.task}")
        run()
        out, err = capsys.readouterr()
        snapshot.assert_match(f"\n{out}")
        snapshot.assert_match(f"\n{err}")


class TestCleanDocker(TaskTests):
    task = "clean_docker"

    def test_execute(self, mock_docker_environment):
        raise NotImplementedError


class ___TestBuildDockerfile(TaskTests):
    """
    Tests for building a project's dockerfile
    """

    task = "build_dockerfile"

    def test_execute(self):
        raise NotImplementedError

    def test_already_built(self):
        """
        If image is built and checkers pass then don't build
        """
        raise NotImplementedError

    def test_builds_for_changes(self):
        """
        If image is built and checkers pass then build
        """
        raise NotImplementedError

    def test_builds_custom_dockerfile(self):
        """
        If image is built and checkers pass then build
        """
        raise NotImplementedError


# TODO: test `remove_app_image`


class ___TestBuildApp(TaskTests):
    """
    Tests the BuildApp virtual task
    """

    task = "build_app"
    # TODO: how to make this generic since it's currently hardcoded with

    def test_execute(self):
        raise NotImplementedError

    def test_execute_with_configured_build_targets(self):
        raise NotImplementedError

    def test_build_failure(self):
        # TODO: test multiple stages
        raise NotImplementedError


@pytest.fixture
def mock_build_task(
    base_mock_ixian_environment, mock_docker_registries, mock_build_image_if_needed,
):
    # mock build_image_if_needed to always build
    (
        mock_image_exists,
        mock_image_exists_in_registry,
        mock_pull_image,
        assert_build,
    ) = mock_build_image_if_needed

    yield (
        assert_build,
        base_mock_ixian_environment,
        mock_docker_registries,
        mock_image_exists,
        mock_image_exists_in_registry,
        mock_pull_image,
    )


class TestBuildBaseImage(TaskTests):
    """
    Tests the `BuildBaseImae` task which builds the base image.
    """

    task = "build_base_image"

    def test_execute(self, mock_cli, mock_build_task):
        CONFIG.DOCKER.DOCKERFILE_BASE = (
            "/opt/ixian_docker/ixian_docker/tests/Dockerfile.one"
        )
        mock_cli.mock_in("build_base_image")
        assert_build, *_ = mock_build_task
        assert_build(CONFIG.DOCKER.BASE_IMAGE)

    def test_custom_tag(self):
        raise NotImplementedError

    def test_custom_repository(self):
        raise NotImplementedError

    def test_build_failure(self):
        raise NotImplementedError

    def test_build_no_pull(self):
        """Build without pulling the remote image"""
        raise NotImplementedError


class ___TestPullAppImage(TaskTests):
    """
    Tests the BuildApp virtual task
    """

    task = "pull"

    def test_execute(self):
        raise NotImplementedError

    def test_custom_app_image(self):
        raise NotImplementedError

    def test_pull_failure(self):
        """
        Failure while transferring image
        """
        raise NotImplementedError

    def test_login_failure(self):
        """
        Failure to authenticate
        """
        raise NotImplementedError


class ___TestPushAppImage(TaskTests):
    """
    Tests the BuildApp virtual task
    """

    task = "push"

    def test_execute(self):
        raise NotImplementedError

    def test_custom_app_image(self):
        raise NotImplementedError

    def test_push_failure(self):
        """
        Failure transferring image.
        """
        raise NotImplementedError

    def test_login_failure(self):
        """
        Failure to authenticate
        """
        raise NotImplementedError

    def test_image_does_not_exist(self):
        """
        Failure to authenticate
        """
        raise NotImplementedError


class ___TestCompose(TaskTests):
    task = "compose"

    def test_execute(self):
        raise NotImplementedError

    def test_execute_image_not_available(self):
        """
        Image should be built if not present.
        """
        raise NotImplementedError


class ___TestBash(TaskTests):
    task = "bash"

    def test_execute(self):
        raise NotImplementedError

    def test_execute_with_args(self):
        """
        args and kwargs are passed to /bin/bash
        :return:
        """
        raise NotImplementedError

    def test_execute_image_not_available(self):
        raise NotImplementedError


class ___TestUp(TaskTests):
    task = "up"

    def test_execute(self):
        raise NotImplementedError

    def test_execute_image_not_available(self):
        raise NotImplementedError


class ___TestDown(TaskTests):
    task = "down"

    def test_execute(self):
        raise NotImplementedError

    def test_execute_image_not_available(self):
        raise NotImplementedError
