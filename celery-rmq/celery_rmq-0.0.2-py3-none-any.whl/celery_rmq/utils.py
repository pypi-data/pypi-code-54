import os

from .errors import ImproperlyConfigured


def get_environment(key, fail_silently=False, default=None):
    """ Get the environment variable or return exception """

    try:
        return os.environ[key]
    except KeyError:
        if not fail_silently:
            raise ImproperlyConfigured
        else:
            return default
