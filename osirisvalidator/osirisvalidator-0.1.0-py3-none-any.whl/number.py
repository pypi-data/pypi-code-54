from osirisvalidator import _
from osirisvalidator.osiris import osiris_validator
from osirisvalidator.exceptions import ValidationException


@osiris_validator
def min_max(func, *args, **kwargs):
    if 'min' not in kwargs:
        raise Exception(_('Min param must be filled.'))

    if 'max' not in kwargs:
        raise Exception(_('Max param must be filled.'))

    message = _('{0} must be between {1} and {2}.'
                .format(kwargs['field'], kwargs['min'], kwargs['max']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if arg2 < int(kwargs['min']) or arg2 > int(kwargs['max']):
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper
