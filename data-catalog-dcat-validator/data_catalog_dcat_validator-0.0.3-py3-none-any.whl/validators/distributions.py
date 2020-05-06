import data_catalog_dcat_validator.errors as validation_errors

from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.models.distribution import Distribution


class DistributionValidator(Validator):
    """Validator for Distribution properties."""

    hint = "Distribution validator"

    def validate(self, value: list) -> None:
        """Validate input."""
        if not isinstance(value, list):
            raise validation_errors.ValidationError.ERROR_VALIDATION

        for dist in value:
            dist = Distribution(dist)
            dist.validate()
