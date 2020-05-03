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

from ixian_docker.tests.conftest import TEST_IMAGE_TWO_NAME
from ixian_docker.modules.docker.checker import DockerImageExists
from ixian_docker.modules.docker.utils.images import image_exists
from ixian_docker.tests.mocks.client import TEST_IMAGE_NAME


class TestDockerImageExists:
    def assert_state(self, snapshot, checker, passes=True):
        snapshot.assert_match(checker.file_path())
        snapshot.assert_match(checker.filename())
        snapshot.assert_match(checker.state())
        snapshot.assert_match(checker.saved_state())
        assert checker.check() == passes

    def test_image_exists(self, mock_get_image, snapshot):
        # check initial state
        checker = DockerImageExists(TEST_IMAGE_NAME)
        self.assert_state(snapshot, checker)

        # recheck state after saving
        checker.save()
        self.assert_state(snapshot, checker)

    def test_image_doesnt_exist(self, snapshot, mock_get_image):
        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_NAME)

        # check initial state
        checker = DockerImageExists(TEST_IMAGE_NAME)
        self.assert_state(snapshot, checker, passes=False)

        # recheck state after saving
        checker.save()
        self.assert_state(snapshot, checker, passes=False)

    def test_image_was_deleted(self, mock_get_image, snapshot):
        """
        Saved state is the image existed. The image doesn't exist now.
        :param test_image:
        :return:
        """
        assert image_exists(TEST_IMAGE_NAME)
        checker = DockerImageExists(TEST_IMAGE_NAME)
        checker.save()

        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_NAME)
        self.assert_state(snapshot, checker, passes=False)

    def test_clone(self, mock_get_image, snapshot):
        checker = DockerImageExists(TEST_IMAGE_NAME)
        clone = checker.clone()

        # state matches original
        assert clone.file_path() == checker.file_path()
        assert clone.filename() == checker.filename()
        assert clone.state() == checker.state()
        assert clone.saved_state() == checker.saved_state()
        assert clone.check() == checker.check()

        # image exists
        self.assert_state(snapshot, clone)
        clone.save()
        self.assert_state(snapshot, clone)

        # image doesnt exist
        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_NAME)
        self.assert_state(snapshot, clone, passes=False)
        clone.save()
        self.assert_state(snapshot, clone, passes=False)

    def test_multiple_images_exist(self, snapshot, mock_get_image):

        checker = DockerImageExists(TEST_IMAGE_NAME, TEST_IMAGE_TWO_NAME)
        self.assert_state(snapshot, checker)
        checker.save()
        self.assert_state(snapshot, checker)

    @pytest.mark.parametrize("not_found_image", [TEST_IMAGE_NAME, TEST_IMAGE_TWO_NAME])
    def test_multiple_only_one_image_exists(
        self, snapshot, mock_get_image, not_found_image
    ):
        mock_get_image.images.get.side_effect.not_found.add(not_found_image)
        assert not image_exists(not_found_image)

        checker = DockerImageExists(TEST_IMAGE_NAME, TEST_IMAGE_TWO_NAME)
        self.assert_state(snapshot, checker, passes=False)
        checker.save()
        self.assert_state(snapshot, checker, passes=False)

    def test_multiple_no_image_exists(self, snapshot, mock_get_image):
        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_NAME)
        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_TWO_NAME)
        assert not image_exists(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_TWO_NAME)

        checker = DockerImageExists(TEST_IMAGE_NAME, TEST_IMAGE_TWO_NAME)
        self.assert_state(snapshot, checker, passes=False)
        checker.save()
        self.assert_state(snapshot, checker, passes=False)

    def test_multiple_clone(self, snapshot, mock_get_image):
        checker = DockerImageExists(TEST_IMAGE_NAME, TEST_IMAGE_TWO_NAME)
        clone = checker.clone()

        # state matches original
        assert clone.file_path() == checker.file_path()
        assert clone.filename() == checker.filename()
        assert clone.state() == checker.state()
        assert clone.saved_state() == checker.saved_state()
        assert clone.check() == checker.check()

        # image exists
        assert image_exists(TEST_IMAGE_NAME)
        assert image_exists(TEST_IMAGE_TWO_NAME)
        self.assert_state(snapshot, clone)
        clone.save()
        self.assert_state(snapshot, clone)

        # image doesnt exist
        mock_get_image.images.get.side_effect.not_found.add(TEST_IMAGE_NAME)
        assert not image_exists(TEST_IMAGE_NAME)
        assert image_exists(TEST_IMAGE_TWO_NAME)
        self.assert_state(snapshot, clone, passes=False)
        clone.save()
        self.assert_state(snapshot, clone, passes=False)


class TestDockerVolumeExists:
    pass
