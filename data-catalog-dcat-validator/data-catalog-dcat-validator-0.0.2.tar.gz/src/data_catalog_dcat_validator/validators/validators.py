import re
import isodate
import data_catalog_dcat_validator.errors as validation_errors
import data_catalog_dcat_validator.models.dcat as dcat

from typing import Any
from data_catalog_dcat_validator.validators.base import Validator


class StringValidator(Validator):
    """Validator for string properties."""

    hint = "String"

    def validate(self, value: str) -> None:
        """Validate input."""
        if not isinstance(value, str):
            raise validation_errors.ValidationError.ERROR_VALIDATION


class IntValidator(Validator):
    """Validator for integer properties."""

    hint = "Integer"

    def validate(self, value: int) -> None:
        """Validate input."""
        if not isinstance(value, int):
            raise validation_errors.ValidationError.ERROR_VALIDATION


class DateValidator(Validator):
    """Validator for date or datetime properties."""

    hint = "ISO date or datetime"

    def validate(self, value: str) -> None:
        """Validate input."""
        try:
            isodate.parse_date(value)
        except Exception:
            try:
                isodate.parse_datetime(value)
            except Exception:
                raise validation_errors.ValidationError.ERROR_VALIDATION


class StringOrListOfStringsValidator(Validator):
    """Validator for string or list of strings properties."""

    hint = "String or list of strings"

    def validate(self, value: Any) -> None:
        """Validate input."""
        if isinstance(value, list):
            for val in value:
                if not isinstance(val, str):
                    raise validation_errors.ValidationError.ERROR_VALIDATION
        else:
            if not isinstance(value, str):
                raise validation_errors.ValidationError.ERROR_VALIDATION


class EmailValidator(Validator):
    """Validator for string with email properties"""

    hint = "String email"

    def validate(self, value: str) -> None:
        """Validate input"""
        if not re.match(r"[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]+", value):
            raise validation_errors.ValidationError.ERROR_VALIDATION


class ContactValidator(Validator):
    """Validator for contact dict properties."""

    hint = "Dict"

    def validate(self, value: dict) -> None:
        """Validate input."""
        if not isinstance(value, dict):
            raise validation_errors.ValidationError.ERROR_VALIDATION

        if not isinstance(value["name"], str):
            raise validation_errors.ValidationError.ERROR_VALIDATION

        if not isinstance(value["mbox"], str):
            raise validation_errors.ValidationError.ERROR_VALIDATION


class DistributionValidator(Validator):
    """Validator for Distribution properties."""

    hint = "Distribution validator"

    def validate(self, value: list) -> None:
        """Validate input."""
        if not isinstance(value, list):
            raise validation_errors.ValidationError.ERROR_VALIDATION

        for dist in value:
            dist = dcat.Distribution(dist)
            dist.validate()


class TemporalValidator(Validator):
    hint = "Temporal validator. keys = ['from', 'to']"

    def validate(self, value: dict) -> None:

        if not isinstance(value, dict):
            raise validation_errors.ValidationError.ERROR_VALIDATION

        if "from" not in list(value.keys()) or "to" not in list(value.keys()):
            raise validation_errors.ValidationError.ERROR_MISSING_PROPERTY


