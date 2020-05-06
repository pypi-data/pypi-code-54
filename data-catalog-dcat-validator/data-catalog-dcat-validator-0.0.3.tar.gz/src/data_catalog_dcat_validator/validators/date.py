from isodate import parse_date, parse_datetime
from isodate.isoerror import ISO8601Error

from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.validators.string import StringValidator
from data_catalog_dcat_validator.errors.exceptions import InvalidValueException


class DateValidator(Validator):
    """Validator for date or datetime properties."""

    hint = "ISO date or datetime"

    def validate(self, value: str) -> None:
        """Validate input."""

        StringValidator().validate(value)

        try:
            parse_date(value)
        except ISO8601Error:
            try:
                parse_datetime(value)
            except ISO8601Error:
                raise InvalidValueException(value)
