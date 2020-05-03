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
from docker import errors as docker_errors

from ixian.tests.conftest import *
from ixian.tests.conftest import mock_environment as base_mock_ixian_environment
from ixian_docker.modules.docker.utils.images import (
    delete_image,
    image_exists,
)
from ixian_docker.tests.mocks.client import *


TEST_IMAGE_NAME = "ixian_docker.tests"
TEST_IMAGE_TWO_NAME = "ixian_docker.tests.two"


# =================================================================================================
# Mock images and Docker api
# =================================================================================================


def build_test_image(
    dockerfile="Dockerfile.one",
    tag=TEST_IMAGE_NAME,
    context="/opt/ixian_docker/ixian_docker/tests/",
    **kwargs,
):
    return build_image(tag=tag, context=context, dockerfile=dockerfile, **kwargs)


def build_test_image_two(
    dockerfile="Dockerfile.two",
    tag=TEST_IMAGE_TWO_NAME,
    context="/opt/ixian_docker/ixian_docker/tests/",
    **kwargs,
):
    return build_image(tag=tag, context=context, dockerfile=dockerfile, **kwargs)


@pytest.fixture
def mock_get_image(mock_docker_environment):
    """
    Mock image TEST_IMAGE_NAME
    """
    not_found = set()

    def get_image_mock(image):
        if image in not_found:
            raise docker_errors.NotFound(image)
        image_mock = mock.Mock()
        image_mock.id = f"MOCK_ID__{image}"
        return image_mock

    get_image_mock.not_found = not_found

    mock_docker_environment.images.get.side_effect = get_image_mock
    yield mock_docker_environment


@pytest.fixture
def mock_image_exists():
    patcher = mock.patch("ixian_docker.modules.docker.utils.images.image_exists")
    mocked = patcher.start()
    mocked.return_value = False
    yield mocked
    mocked.stop()


@pytest.fixture
def mock_image_exists_in_registry():
    patcher = mock.patch(
        "ixian_docker.modules.docker.utils.images.image_exists_in_registry"
    )
    mocked = patcher.start()
    mocked.return_value = False
    yield mocked
    mocked.stop()


@pytest.fixture
def mock_pull_image():
    patcher = mock.patch("ixian_docker.modules.docker.utils.images.pull_image")
    mocked = patcher.start()
    mocked.return_value = False
    yield mocked
    mocked.stop()


@pytest.fixture
def test_image():
    """
    Sets up a real docker image by building it.
    """
    yield build_test_image()
    delete_image(TEST_IMAGE_NAME, force=True)


@pytest.fixture
def test_image_two():
    """
    Sets up a real docker image by building it.
    """
    yield build_test_image_two()
    delete_image(TEST_IMAGE_TWO_NAME, force=True)


@pytest.fixture(
    params=[
        "image_exists",
        "image_exists_local",
        "image_does_not_exist",
        "pull_image",
        "pull_image_not_found",
    ]
)
def mock_build_image_if_needed(
    request,
    mock_image_exists,
    mock_image_exists_in_registry,
    mock_pull_image,
    capsys,
    snapshot,
):
    mock_image_exists.return_value = False
    mock_image_exists_in_registry.return_value = False

    if request.param == "image_exists_local":
        mock_image_exists.return_value = True
        mock_image_exists_in_registry.return_value = False
    if request.param == "image_exists":
        mock_image_exists.return_value = True
        mock_image_exists_in_registry.return_value = True
    elif request.param == "image_does_not_exist":
        pass
    elif request.param == "pull_image":
        mock_image_exists_in_registry.return_value = True
    elif request.param == "pull_image_not_found":
        mock_image_exists_in_registry.return_value = True
        mock_pull_image.side_effect = docker_errors.NotFound("testing")
    elif request.param == "pull_unknown_registry":
        raise NotImplementedError

    image_will_be_built = request.param in {
        "image_does_not_exist",
        "pull_image_not_found",
    }

    def assert_build(image):
        from ixian.runner import run

        if image_will_be_built:
            image_exists_ = image_exists
        else:
            image_exists_ = mock_image_exists

        assert not image_exists(image)
        try:
            run()
        except:
            raise
        else:
            if image_will_be_built:
                assert image_exists(image)
            else:
                assert not image_exists(image)
        finally:
            if image_will_be_built:
                delete_image(CONFIG.DOCKER.BASE_IMAGE)
        assert not image_exists(image)

        out, err = capsys.readouterr()
        snapshot.assert_match(f"\n{out}")
        snapshot.assert_match(f"\n{err}")
        snapshot.assert_match(mock_image_exists.call_args_list)
        snapshot.assert_match(mock_image_exists_in_registry.call_args_list)
        snapshot.assert_match(mock_pull_image.call_args_list)

    yield mock_image_exists, mock_image_exists_in_registry, mock_pull_image, assert_build


# =================================================================================================
# Mock module environments
# =================================================================================================


@pytest.fixture
def mock_environment(base_mock_ixian_environment):
    load_module("ixian_docker.modules.docker")
    yield base_mock_ixian_environment


@pytest.fixture
def mock_npm_environment(mock_environment):
    load_module("ixian_docker.modules.npm")
    yield mock_environment


@pytest.fixture
def mock_bower_environment(mock_npm_environment):
    load_module("ixian_docker.modules.bower")
    yield mock_npm_environment


@pytest.fixture
def mock_jest_environment(mock_npm_environment):
    load_module("ixian_docker.modules.jest")
    yield mock_npm_environment


@pytest.fixture
def mock_eslint_environment(mock_npm_environment):
    load_module("ixian_docker.modules.eslint")
    yield mock_npm_environment


@pytest.fixture
def mock_webpack_environment(mock_npm_environment):
    load_module("ixian_docker.modules.webpack")
    yield mock_npm_environment


@pytest.fixture
def mock_python_environment(mock_environment):
    load_module("ixian_docker.modules.python")
    yield mock_environment


@pytest.fixture
def mock_django_environment(mock_python_environment):
    load_module("ixian_docker.modules.django")
    yield mock_python_environment
