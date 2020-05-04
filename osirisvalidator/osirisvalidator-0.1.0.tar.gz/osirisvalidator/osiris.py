from osirisvalidator import _


def osiris_validator(decorator):

    def maker(*args, **kwargs):
        if 'field' not in kwargs:
            raise Exception(_('arg field is missing'))

        def wrapper(fn):
            return decorator(fn, *args, **kwargs)

        return wrapper

    return maker
