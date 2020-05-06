from osirisvalidator import _
from osirisvalidator.osiris import osiris_validator
from osirisvalidator.exceptions import ValidationException


@osiris_validator
def min_max(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if arg2 is not None:

            if arg2 < int(kwargs['min']) or arg2 > int(kwargs['max']):
                raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def not_null(func, *args, **kwargs):

    message = _('{0} cannot be null.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if arg2 is None:
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper
