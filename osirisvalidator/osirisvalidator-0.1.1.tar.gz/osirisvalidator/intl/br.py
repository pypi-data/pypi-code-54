from osirisvalidator import _
from osirisvalidator.osiris import osiris_validator
from osirisvalidator.exceptions import ValidationException


@osiris_validator
def valid_cpf(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isdigit():
            raise ValidationException(kwargs['field'], message)

        if len(arg2) != 11:
            raise ValidationException(kwargs['field'], message)

        if arg2 in [s * 11 for s in [str(n) for n in range(10)]]:
            raise ValidationException(kwargs['field'], message)

        calc = [i for i in range(1, 10)]
        d1 = sum([int(a) * (11 - b) for a, b in zip(arg2[:-2], calc)]) % 11
        d1 = 0 if d1 < 2 else (11 - d1)
        calc = [i for i in range(1, 11)]
        d2 = sum([int(a) * (12 - b) for a, b in zip(arg2[:-1], calc)]) % 11
        d2 = 0 if d2 < 2 else (11 - d2)

        if str(d1) != arg2[-2] or str(d2) != arg2[-1]:
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def valid_cnpj(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isdigit():
            raise ValidationException(kwargs['field'], message)

        if len(arg2) != 14:
            raise ValidationException(kwargs['field'], message)

        if arg2 in [s * 14 for s in [str(n) for n in range(13)]]:
            raise ValidationException(kwargs['field'], message)

        f_dv = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        d1 = sum([int(a) * b for a, b in zip(arg2[:-2], f_dv)]) % 11
        d1 = 0 if d1 < 2 else (11 - d1)
        f_dv = [6] + f_dv
        d2 = sum([int(a) * b for a, b in zip(arg2[:-1], f_dv)]) % 11
        d2 = 0 if d2 < 2 else (11 - d2)

        if str(d1) != arg2[-2] or str(d2) != arg2[-1]:
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper


@osiris_validator
def valid_cep(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not arg2.isdigit():
            raise ValidationException(kwargs['field'], message)

        if len(arg2) != 8:
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper
