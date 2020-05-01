import pathlib
from typing import Optional

from .errors import ValidationError


class IsInstance:
    def __init__(self, dtype=None, message: Optional[str] = None):
        self._dtype = dtype
        self._message = message

    def __call__(self, config, value) -> None:
        if self._dtype is not None and not isinstance(value, self._dtype):
            message = self._message
            if message is None:
                message = "value must be of type {dtype} ({value})"
            raise ValidationError(message.format(dtype=self._dtype, value=value))


class GreaterThan:
    def __init__(self, field_name, message=None):
        self._field_name = field_name
        self._message = message

    def __call__(self, config, value):
        try:
            other_value = config[self._field_name].data
        except KeyError:
            raise ValidationError("unknown field name ({0})".format(self._field_name))

        if value <= other_value:
            raise ValidationError(self._message)


class Range:
    def __init__(
        self,
        lower: Optional[float] = None,
        upper: Optional[float] = None,
        message: Optional[str] = None,
    ):
        self._lower = lower
        self._upper = upper
        self._message = message

    def __call__(self, config, value) -> None:
        lower, upper = self._lower, self._upper
        if (lower is not None and value < lower) or (
            upper is not None and value > upper
        ):
            message = self._message
            if message is None:
                if upper is None:
                    message = "value must be at least {lower} ({value})"
                elif lower is None:
                    message = "value must be less than {upper} ({value})"
                else:
                    message = "value must be between {lower} and {upper} ({value})"
            raise ValidationError(message.format(lower=lower, upper=upper, value=value))


class Length:
    def __init__(
        self,
        lower: Optional[int] = None,
        upper: Optional[int] = None,
        message: Optional[str] = None,
    ):
        self._lower = lower
        self._upper = upper
        self._message = message

    def __call__(self, config, value) -> None:
        lower, upper = self._lower, self._upper
        length = len(value)

        if (lower is not None and length < lower) or (
            upper is not None and length > upper
        ):
            message = self._message
            if message is None:
                if upper is None:
                    message = "length must be at least {lower} ({length})"
                elif lower is None:
                    message = "length must be less than {upper} ({length})"
                else:
                    message = "length must be between {lower} and {upper} ({length})"
            raise ValidationError(
                message.format(lower=lower, upper=upper, length=length)
            )


class OneOf:
    def __init__(self, choices, message=None):
        self._choices = choices
        self._message = message

    def __call__(self, config, value) -> None:
        if value not in self._choices:
            message = self._message
            if message is None:
                message = "value must be one of {{{choices}}} ({value})"
            raise ValidationError(
                message.format(
                    choices=", ".join([str(c) for c in self._choices]), value=value
                )
            )


class Path:
    def __init__(
        self,
        file_okay: bool = True,
        dir_okay: bool = True,
        exists: bool = True,
        message: Optional[str] = None,
    ):
        self._file_okay = file_okay
        self._dir_okay = dir_okay
        self._exists = exists

        self._message = message

    def __call__(self, config, value) -> None:
        path = pathlib.Path(value)

        if path.exists() and (
            not self._exists
            or (not self._file_okay and path.is_file())
            or (not self._dir_okay and path.is_dir())
        ):
            message = self._message
            if message is None:
                if not self._exists:
                    message = "path already exists ({value})"
                elif not self._file_okay and path.is_file():
                    message = "must be a directory ({value})"
                elif not self._dir_okay and path.is_dir():
                    message = "must be a file ({value})"
            raise ValidationError(message.format(value=str(path)))
        elif not path.exists() and self._exists:
            raise ValidationError("path must exists".format(value=str(value)))
