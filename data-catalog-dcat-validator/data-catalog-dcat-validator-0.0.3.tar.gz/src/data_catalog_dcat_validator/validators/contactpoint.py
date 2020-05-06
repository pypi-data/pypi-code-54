from data_catalog_dcat_validator.models.contactpoint import ContactPointModel
from data_catalog_dcat_validator.validators.base import Validator


class ContactValidator(Validator):
    """Validator for contact dict properties."""

    hint = "Dict"

    def validate(self, value: dict) -> None:
        ContactPointModel(value).validate()
