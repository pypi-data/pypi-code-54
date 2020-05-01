
from my_money.errors import InputError


def _veryfy_input_type(value, _type):
    try:
        return _type(value)
    except (ValueError, TypeError):
        raise InputError(f"Entered data not match desired type {_type}: {value}")


def _verify_max_limit(value, _max):
    if max is not None:
        assert value <= max, f"Entered value not match limitation (Entered: {value} larger then {_max}"


def _confirm_value(silent):
    if silent:
        confirm = input("Are you sure (y/n)?")
        if confirm.lower() != "y":
            raise InputError("User not confirmed value")


# TODO: Solve verification for 'min'
# TODO: Solve verification for 'min/max' in case input type - str

def get_input(prompt, **kwargs):
    """

    :param prompt:
    :param kwargs:
    :return:
    """
    _type = kwargs.get('type', str)
    retry_count = kwargs.get('retry_count', 5)
    silent = kwargs.get('silent', False)
    _max = kwargs.get('max', None)
    _min = kwargs.get('min', None)

    down_counter = retry_count
    while down_counter > 0:
        try:
            temp = input(prompt)
            temp = _veryfy_input_type(temp, _type)
            _verify_max_limit(temp, _max)
            _confirm_value(silent)

            return temp
        except AssertionError as e:
            print(f"{e}")
        down_counter -= 1
    raise Exception(f"after the {retry_count} tries you need to start over")


__all__ = [
    get_input.__name__
]


