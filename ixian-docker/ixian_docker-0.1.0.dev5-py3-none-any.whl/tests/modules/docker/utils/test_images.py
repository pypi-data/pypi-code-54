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

from docker.errors import NotFound as DockerNotFound

from ixian.utils.filesystem import pwd
from ixian_docker.tests.conftest import TEST_IMAGE_NAME, build_test_image
from ixian_docker.modules.docker.utils.images import (
    image_exists,
    push_image,
    pull_image,
    image_exists_in_registry,
    delete_image,
    parse_registry,
    build_image_if_needed,
    build_image,
)
from ixian_docker.tests import event_streams


class TestImageExists:
    """
    Tests for image existing locally
    """

    def test_image_does_not_exist(self):
        # delete images to ensure no leakage from other tests
        delete_image(TEST_IMAGE_NAME, force=True)
        assert not image_exists(TEST_IMAGE_NAME)

    def test_image_exists(self, test_image):
        assert image_exists(TEST_IMAGE_NAME)


class TestBuildImage:
    def test_build_image(self):
        # test_image fixture builds the image, just check if it exists
        tag = f"{TEST_IMAGE_NAME}:latest"
        assert not image_exists(TEST_IMAGE_NAME)
        assert not image_exists(tag)
        try:
            build_test_image(tag=tag)
            assert image_exists(TEST_IMAGE_NAME)
            assert image_exists(tag)
        finally:
            delete_image(tag, force=True)
            delete_image(TEST_IMAGE_NAME, force=True)
            assert not image_exists(TEST_IMAGE_NAME)
            assert not image_exists(tag)

    def test_build_image_default_context(self, mock_docker_environment):
        """
        When context=None then the PWD is used for the context
        """
        build_image("Dockerfile.test", TEST_IMAGE_NAME, context=None)
        mock_docker_environment.images.build.assert_called_with(
            dockerfile="Dockerfile.test", path=pwd(), tag=TEST_IMAGE_NAME
        )

    def test_build_image_custom_tag(self):
        tag = f"{TEST_IMAGE_NAME}:custom"
        assert not image_exists(TEST_IMAGE_NAME)
        assert not image_exists(tag)
        try:
            build_test_image(tag=tag)
            assert image_exists(tag)
            # image_exists only returns True for "latest" if no tag is given
            assert not image_exists(TEST_IMAGE_NAME)
        finally:
            delete_image(tag, force=True)
            delete_image(TEST_IMAGE_NAME, force=True)
            assert not image_exists(TEST_IMAGE_NAME)
            assert not image_exists(tag)


class TestDeleteImage:
    def test_delete_image(self, test_image):
        assert image_exists(TEST_IMAGE_NAME)
        assert delete_image(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_NAME)

    def test_force_delete_image(self, test_image):
        assert image_exists(TEST_IMAGE_NAME)
        assert delete_image(TEST_IMAGE_NAME, force=True)
        assert not image_exists(TEST_IMAGE_NAME)

    def test_delete_image_that_does_not_exist(self):
        # delete returns false if no image was deleted
        assert not image_exists(TEST_IMAGE_NAME)
        assert not delete_image(TEST_IMAGE_NAME)
        assert not delete_image(TEST_IMAGE_NAME, force=True)

    def test_delete_latest(self, test_image):
        """
        The image tagged with latest may be deleted using that tag.
        """
        tag = f"{TEST_IMAGE_NAME}:latest"
        assert image_exists(TEST_IMAGE_NAME)
        assert image_exists(tag)
        assert delete_image(tag, force=True)
        assert not image_exists(TEST_IMAGE_NAME)
        assert not image_exists(tag)

    def test_delete_image_by_wrong_tag(self, test_image):
        """
        Only images with the matching tag are deleted if one is specified
        """
        tag = f"{TEST_IMAGE_NAME}:wrong_tag"
        assert image_exists(TEST_IMAGE_NAME)
        assert not delete_image(tag, force=True)
        assert image_exists(TEST_IMAGE_NAME)

        # now delete using that tag, both tags will be gone because it's the same image.
        build_test_image(tag=tag)
        assert image_exists(TEST_IMAGE_NAME)
        assert image_exists(tag)
        assert delete_image(tag, force=True)
        assert not image_exists(TEST_IMAGE_NAME)
        assert not image_exists(tag)


class TestBuildImageIfNeeded:

    default_image = f"{TEST_IMAGE_NAME}:latest"
    default_call_kwargs = dict(
        dockerfile="Dockerfile", path="/opt/ixian_docker", tag=default_image
    )

    def test_image_exists_local(self, mock_docker_environment):
        """
        If image exists locally, nothing is done.
        """
        build_image_if_needed(TEST_IMAGE_NAME)
        mock_docker_environment.images.build.assert_not_called()

    def test_image_exists_registry(self, mock_docker_environment):
        """
        If doesn't exist locally but  exists in the repository, it will be pulled.
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        build_image_if_needed(TEST_IMAGE_NAME)
        mock_docker_environment.api.pull.assert_called_with(
            TEST_IMAGE_NAME, "latest", decode=True, stream=True
        )
        mock_docker_environment.images.build.assert_not_called()

    def test_image_exists_registry_pull_not_found(self, mock_docker_environment):
        """
        If the image exists in the registry, but for some reason pull returns DockerNotFound, then
        fall back to building. This shouldn't happen in practice, but it's coded defensively just
        in case of some weirdness.
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        mock_docker_environment.api.pull.side_effect = DockerNotFound("testing")

        build_image_if_needed(TEST_IMAGE_NAME)
        mock_docker_environment.api.pull.assert_called_with(
            TEST_IMAGE_NAME, "latest", decode=True, stream=True
        )
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_image_exists_registry_no_pull(self, mock_docker_environment):
        """
        Don't check for a remote image or pull it if pull=False. Even if the image exists remotely
        a new image will be built.
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        build_image_if_needed(TEST_IMAGE_NAME, pull=False)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_image_exists_local_and_registry(self, mock_docker_environment):
        """
        If image exists locally, nothing is done.
        """
        build_image_if_needed(TEST_IMAGE_NAME)
        mock_docker_environment.images.build.assert_not_called()

    def test_image_does_not_exist(self, mock_docker_environment):
        """
        If image doesn't exist anywhere then build.
        :return:
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        mock_docker_environment.images.get_registry_data.side_effect = DockerNotFound(
            "mocked"
        )
        build_image_if_needed(TEST_IMAGE_NAME)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

        build_image_if_needed(TEST_IMAGE_NAME, pull=True)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_force_with_local_image(self, mock_docker_environment):
        """
        if force=True then image will always build
        """
        build_image_if_needed(TEST_IMAGE_NAME, force=True)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_force_with_registry_image(self, mock_docker_environment):
        """
        if force=True then image will always build
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        build_image_if_needed(TEST_IMAGE_NAME, force=True)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_force_with_local_and_registry_image(self, mock_docker_environment):
        """
        if force=True then image will always build
        """
        build_image_if_needed(TEST_IMAGE_NAME, force=True)
        mock_docker_environment.images.build.assert_called_with(
            **self.default_call_kwargs
        )

    def test_unknown_registry(self, mock_docker_environment):
        """
        If the registry isn't configured, always build
        """
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        build_image_if_needed("unknown.registry.com/foo/bar")
        mock_docker_environment.images.build.assert_called_with(
            dockerfile="Dockerfile",
            tag="unknown.registry.com/foo/bar:latest",
            path="/opt/ixian_docker",
        )

    def test_recheck_fails(self):
        """
        After pulling a re-check is run. If it fails the image is built.
        """
        raise NotImplementedError

    def test_custom_tag(self, mock_docker_environment):
        tag = f"{TEST_IMAGE_NAME}:custom_tag"
        mock_docker_environment.images.get.side_effect = DockerNotFound("testing")
        mock_docker_environment.images.get_registry_data.side_effect = DockerNotFound(
            "mocked"
        )
        build_image_if_needed(TEST_IMAGE_NAME, "custom_tag")
        mock_docker_environment.images.build.assert_called_with(
            dockerfile="Dockerfile", path="/opt/ixian_docker", tag=tag
        )

        build_image_if_needed(TEST_IMAGE_NAME, "custom_tag", pull=True)
        mock_docker_environment.images.build.assert_called_with(
            dockerfile="Dockerfile", path="/opt/ixian_docker", tag=tag
        )


class TestParseRegistry:
    def test_parse_repository(self):
        assert parse_registry("foo.bar.com/test/image") == "foo.bar.com"
        assert parse_registry("foo.bar.com/test/image") == "foo.bar.com"
        assert parse_registry("foo.bar.com/test_image") == "foo.bar.com"
        assert parse_registry("192.168.1.1/test/image") == "192.168.1.1"
        assert parse_registry("192.168.1.1/test_image") == "192.168.1.1"
        assert parse_registry("foo.bar.com") == "foo.bar.com"
        assert parse_registry("192.168.1.1") == "192.168.1.1"

    def test_parse_no_registry(self):
        """
        If there is no hostname in the image name then the default repository is used.
        """
        assert parse_registry("image_name_without_hostname") == "docker.io"
        assert parse_registry("image_name_without_hostname/foo") == "docker.io"
        assert parse_registry("image_name_without_hostname/foo/bar") == "docker.io"
        assert parse_registry("imagenamewithouthostname/foo/bar") == "docker.io"
        assert parse_registry("imagenamewithouthostname/foo") == "docker.io"
        assert parse_registry("imagenamewithouthostname") == "docker.io"


class TestImageExistsInRegistry:
    """
    Tests for image existing on remote registry
    """

    def test_image_exists(self, mock_docker_environment):
        assert image_exists_in_registry(TEST_IMAGE_NAME) is True

    def test_image_does_not_exist(self, mock_docker_environment):
        mock_docker_environment.images.get_registry_data.side_effect = DockerNotFound(
            "mocked"
        )
        assert image_exists_in_registry(TEST_IMAGE_NAME) is False


class TestPush:
    """
    Tests for pushing image to registry
    """

    def test_push(self, mock_docker_environment, snapshot, capsys):
        """
        Test a successful push
        """
        push_image(TEST_IMAGE_NAME)
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_push_already_pushed(self, mock_docker_environment, snapshot, capsys):
        """
        Test a successful push where all layers already exist on the registry
        """
        mock_docker_environment.api.push = mock.Mock(
            return_value=event_streams.PUSH_ALREADY_PRESENT
        )
        push_image(TEST_IMAGE_NAME)
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_push_tag(self, mock_docker_environment, snapshot, capsys):
        """
        Test pushing with an explicit tag
        """
        mock_docker_environment.api.push = mock.Mock(
            return_value=event_streams.PUSH_SUCCESSFUL_CUSTOM_TAG
        )
        push_image(TEST_IMAGE_NAME, "custom_tag")
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_push_error(self, mock_docker_environment, snapshot, capsys):
        """
        Test a push with an error
        """
        mock_docker_environment.api.push = mock.Mock(
            return_value=event_streams.ECR_PUSH_AUTH_FAILURE
        )
        push_image(TEST_IMAGE_NAME, "custom_tag")
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_push_silent(self, mock_docker_environment, snapshot, capsys):
        """
        Test a successful push with silent=True
        """
        push_image(TEST_IMAGE_NAME, silent=True)
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_push_error_and_silent(self, mock_docker_environment, snapshot, capsys):
        """
        Test a push with an error while silent=True
        """
        mock_docker_environment.api.push = mock.Mock(
            return_value=event_streams.ECR_PUSH_AUTH_FAILURE
        )
        push_image(TEST_IMAGE_NAME, "custom_tag", silent=True)
        out, err = capsys.readouterr()
        snapshot.assert_match(out)


class TestPull:
    """
    Tests for pulling image from registry
    """

    def test_pull(self, mock_docker_environment, snapshot, capsys):
        """
        Test a successful push
        """
        mock_client = mock_docker_environment
        pull_image(TEST_IMAGE_NAME)
        mock_client.api.pull.assert_called_with(
            TEST_IMAGE_NAME, "latest", stream=True, decode=True
        )
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_pull_silent(self, mock_docker_environment, snapshot, capsys):
        """
        Test a successful push with silent=True
        """
        mock_client = mock_docker_environment
        pull_image(TEST_IMAGE_NAME, silent=True)
        mock_client.api.pull.assert_called_with(
            TEST_IMAGE_NAME, "latest", stream=False, decode=False
        )
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_pull_tag(self, mock_docker_environment, snapshot, capsys):
        """
        Test pushing with an explicit tag
        """
        mock_client = mock_docker_environment
        pull_image(TEST_IMAGE_NAME, "custom_tag")
        mock_client.api.pull.assert_called_with(
            TEST_IMAGE_NAME, "custom_tag", stream=True, decode=True
        )
        out, err = capsys.readouterr()
        snapshot.assert_match(out)

    def test_pull_error(self):
        """
        Test a push with an error
        """
        raise NotImplementedError

    def test_pull_error_and_silent(self, mock_docker_environment, snapshot, capsys):
        """
        Test a push with an error while silent=True
        """
        raise NotImplementedError
