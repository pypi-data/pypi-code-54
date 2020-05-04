from osirisvalidator import _
from osirisvalidator.osiris import osiris_validator
from osirisvalidator.exceptions import ValidationException
import re


@osiris_validator
def not_empty(func, *args, **kwargs):
    message = _('{0} may not be empty.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if arg2 is None or len(arg2) == 0:
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def not_blank(func, *args, **kwargs):
    message = _('{0} may not be blank.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if arg2 is None or len(arg2.strip()) == 0:
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def is_alpha(func, *args, **kwargs):
    message = _('{0} must contain only letters.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isalpha():
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def is_alpha_space(func, *args, **kwargs):
    message = _('{0} must contain only letters.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.replace(" ", "").isalpha():
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def is_alnum(func, *args, **kwargs):
    message = _('{0} must contain only letters and digits.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isalnum():
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def is_alnum_space(func, *args, **kwargs):
    message = _('{0} must contain only letters and digits.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.replace(" ", "").isalnum():
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def is_digit(func, *args, **kwargs):
    message = _('{0} must contain only digits.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isdigit():
            raise ValidationException(kwargs['field'], message)
        else:
            return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def string_len(func, *args, **kwargs):
    if 'min' not in kwargs:
        raise Exception(_('Min param must be filled.'))

    if 'max' not in kwargs:
        raise Exception(_('Max param must be filled.'))

    message = _('{0} must be a minimum of {1} characters and a maximum of {2}.'
                .format(kwargs['field'], kwargs['min'], kwargs['max']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if len(arg2) < int(kwargs['min']) or len(arg2) > int(kwargs['max']):
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def match_regex(func, *args, **kwargs):
    if 'regex' not in kwargs:
        raise Exception(_('Regex param must be filled.'))

    message = _('{0} is incorrect.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not re.match(kwargs['regex'], arg2):
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper
