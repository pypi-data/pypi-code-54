from osirisvalidator import _
from osirisvalidator.osiris import osiris_validator
from osirisvalidator.exceptions import ValidationException
import re


@osiris_validator
def valid_email(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", arg2):
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper
