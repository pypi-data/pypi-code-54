from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Any

from data_catalog_dcat_validator.errors.exceptions import InvalidValueException, ErrorInvalidPropertyException, \
    WarningMissingRecommendedPropertyException, InvalidTypeException, ErrorMissingPropertyException, ErrorType
from data_catalog_dcat_validator.validators.string import StringValidator
from data_catalog_dcat_validator.validators.base import Validator


class BaseModel(ABC):
    """
    A model has to have more than one field.'
    """
    def __init__(self, metadata: dict):
        self.metadata = metadata

    @property
    @abstractmethod
    def mandatory_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def recommended_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def optional_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def validators(self):
        raise NotImplementedError()

    @abstractmethod
    def report_errors(self, errors):
        raise NotImplementedError()

    def get_validator(self, key: Any) -> Validator:
        """Get validator for key. If key not does not exist then StringValidator"""

        validator = self.validators.get(key, StringValidator())

        return validator

    def get_properties(self) -> List:
        """Get list of all properties."""
        return [*self.mandatory_fields, *self.recommended_fields, *self.optional_fields]

    def validate_content(self, errors: Dict) -> None:
        """Check if mandatory and recommended properties are included."""

        try:
            self._check_mandatory_fields()
        except ErrorMissingPropertyException as err:
            errors[err.code].append({"field": err.values})

        try:
            self._check_recommended_fields()
        except WarningMissingRecommendedPropertyException as err:
            errors[err.code].append({"field": err.values})

        try:
            self._invalid_fields()
        except ErrorInvalidPropertyException as err:
            errors[err.code].append({"field": err.values})

    def validate(self):
        errors = defaultdict(list)

        self.validate_content(errors)

        for field, val in self.metadata.items():
            try:
                self.get_validator(field).validate(val)
            except InvalidTypeException as err:
                errors[err.code].append({"field": field, "expected": err.expected_type})
            except InvalidValueException as err:
                errors[err.code].append({"field": field})

        self.report_errors(errors)

        return errors

    def _invalid_fields(self):
        non_dcat_fields = [field for field in self.metadata.keys() if field not in self.get_properties()]
        if non_dcat_fields:
            raise ErrorInvalidPropertyException(non_dcat_fields)

    def _check_mandatory_fields(self):
        missing_mandator_fields = [field for field in self.mandatory_fields if field not in self.metadata.keys()]
        if missing_mandator_fields:
            raise ErrorMissingPropertyException(missing_mandator_fields)

    def _check_recommended_fields(self):
        missing_recommended_fields = [field for field in self.recommended_fields if field not in self.metadata.keys()]
        if missing_recommended_fields:
            raise WarningMissingRecommendedPropertyException(missing_recommended_fields)

    @staticmethod
    def _error_to_string(code: str, fields: List) -> str:
        """Errors to string."""

        items = []
        for field in fields:
            if field.get("validator"):
                items.append({field['validator'].hint: field['field']})
            else:
                items.append(field['field'])
        if code == ErrorType.ERROR_MISSING_PROPERTY.value:
            return f"Missing mandatory props(s): {items}"
        elif code == ErrorType.WARNING_MISSING_RECOMMENDED_PROPERTY.value:
            return f"Missing recommended props(s): {items}"
        elif code == ErrorType.ERROR_INVALID_VALUE.value:
            return f"Not valid: {field}"
        elif code == ErrorType.ERROR_OTHER.value:
            return f"Could not be validated: {items}"
        elif code == ErrorType.ERROR_VALIDATION.value:
            return f"Invalid type: {items}"
        elif code == ErrorType.ERROR_INVALID_PROPERTY.value:
            return f"Property not in DCAT schema: {items}"
