from importlib import import_module
from invisibleroads_macros_log import get_log
from invisibleroads_macros_security import make_random_string
from os.path import expandvars

from .constants import SECRET_LENGTH


L = get_log(__name__)


class Settings(dict):

    def set(self, settings, prefix, key, default=None, parse=None):
        value = set_default(settings, prefix + key, default, parse)
        self[key] = value
        return value


def set_default(settings, key, default, parse=None):
    value = settings.get(key, default)
    if key not in settings:
        L.warning(f'using default {key} = {value}')
    elif value in ('', None):
        L.warning(f'missing {key}')
    elif parse:
        value = parse(value)
    settings[key] = value
    return value


def fill_environment_variables(settings):
    return {
        k: expandvars(v)
        if isinstance(v, str) else v
        for k, v in settings.items()
    }


def fill_secrets(settings, secret_length=SECRET_LENGTH):
    return {
        k: make_random_string(secret_length)
        if k.endswith('.secret') and not v else v
        for k, v in settings.items()
    }


def fill_extensions(settings):

    def load_extensions(extension_specs):
        extensions = []
        for extension_spec in extension_specs:
            module_spec, extension_name = extension_spec.rsplit(
                '.', maxsplit=1)
            module = import_module(module_spec)
            extensions.append(getattr(module, extension_name))
        return extensions

    return {
        k: load_extensions(v.split())
        if k.endswith('.extensions') else v
        for k, v in settings.items()
    }
