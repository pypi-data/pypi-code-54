"""Test configuration loader."""

import os
import shutil
import tempfile

import pytest
from mock import patch
from pkg_resources import EntryPoint

from config_loader import Config


@pytest.fixture(scope='function')
def config():
    """Configuration object."""
    return Config()


class ConfigEP(EntryPoint):
    """Mocking of entrypoint."""

    def __init__(self, name=None, module_name=None, **kwargs):
        """Save keyword arguments as config."""
        self.name = name
        self.module_name = module_name
        self.kwargs = kwargs

    def __str__(self):
        """Mock __str__ method."""
        return self.name or ''

    def load(self):
        """Mock load entry point."""

        class Config(object):
            pass

        for key, val in self.kwargs.items():
            setattr(Config, key, val)
        return Config


def _mock_ep(eps):
    """Mock for pkg_resources.iter_entry_points."""

    def iter_entry_points(name):
        for ep in eps:
            yield ep

    return iter_entry_points


def test_defaults():
    """Test defaults values are inside config object."""
    config = Config(
        env_var='DO_NOT_USE',
        env_prefix='DO_NOT_USE',
        entry_point_name='DO_NOT_USE',
    )

    assert not config.keys()


def test_object(config):
    """Test from object."""

    class Config(object):
        TESTVAR = True

    assert not config.get('TESTVAR', False)
    config.from_object(Config)
    assert config.get('TESTVAR', False)


def test_entry_point(config):
    """Test entry point."""
    assert not config.get('TESTVAR_EP', False)
    # Load mock entrypoint
    with patch(
        'pkg_resources.iter_entry_points',
        _mock_ep([ConfigEP(TESTVAR_EP=True)]),
    ):
        config.from_entry_point('test')
        assert config.get('TESTVAR_EP', False)


def test_env(config):
    """Test environment variables."""
    assert not config.get('MYPREFIX_TESTVAR', False)

    os.environ['MYPREFIX_TESTVAR'] = 'True'
    os.environ['MYPREFIX_JUSTASTRING'] = 'This is just a string'
    os.environ[
        'MYPREFIX_COMPLEX_DICT'
    ] = "{'complex': {'python': 'dict'}, 'with': ['list', 'and', 1234]}"

    config.from_env(prefix='MYPREFIX_')

    assert config.get('TESTVAR') is True
    assert config.get('JUSTASTRING') == "This is just a string"
    assert config.get('COMPLEX_DICT') == {
        'complex': {'python': 'dict'},
        'with': ['list', 'and', 1234],
    }


def test_file(config):
    """Tes file."""
    assert not config.get('TESTVAR_CONFIG', False)
    try:
        tmp_path = tempfile.mkdtemp()
        # Write config into instance folder.
        with open(os.path.join(tmp_path, 'testapp.cfg'), 'w') as f:
            f.write("TESTVAR_CONFIG = True\n")

        config.from_pyfile(filename=os.path.join(tmp_path, 'testapp.cfg'))
        assert config.get('TESTVAR_CONFIG', False)
    finally:
        shutil.rmtree(tmp_path)


def test_envvar(config):
    """Tes environment variable file."""
    assert not config.get('TESTVAR_CONFIG_ENVVAR', False)
    try:
        tmp_path = tempfile.mkdtemp()
        # Write config into instance folder.
        with open(os.path.join(tmp_path, 'testapp.cfg'), 'w') as f:
            f.write("TESTVAR_CONFIG_ENVVAR = True\n")

        os.environ['MYPREFIX_TEST_CONFIG'] = os.path.join(
            tmp_path, 'testapp.cfg'
        )

        config.from_envvar(variable_name='MYPREFIX_TEST_CONFIG')
        assert config.get('TESTVAR_CONFIG_ENVVAR', False)
    finally:
        shutil.rmtree(tmp_path)
