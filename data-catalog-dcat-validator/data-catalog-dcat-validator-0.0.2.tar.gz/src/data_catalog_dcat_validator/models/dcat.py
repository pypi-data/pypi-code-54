"""
Deetly dcat.

Utility functions for validating dcat formated metadata
"""
import data_catalog_dcat_validator.validators.validators as validators
import data_catalog_dcat_validator.errors as validation_errors

from data_catalog_dcat_validator.validators.base import Validator
from collections import defaultdict
from typing import Any, Dict, List


class DcatModel:
    """DCAT model."""

    def __init__(self, metadata: dict) -> None:
        """Constructor."""
        self.metadata = metadata
        self.mandatory = []
        self.recommended = []
        self.optional = []
        self.validators = {
            # 'accessRights': validators.StringValidator(),
            # 'accessService': validators.StringValidator(),
            # 'accessURL': validators.StringValidator(),
            # 'accrualPeriodicity': validators.StringValidator(),
            # 'availability': validators.StringValidator(),
            "byteSize": validators.IntValidator(),
            # 'checksum': validators.StringValidator(),
            # 'compressFormat': validators.StringValidator(),
            # 'conformsTo': validators.StringValidator(),
            "contactPoint": validators.ContactValidator(),
            # 'creator': validators.StringValidator(),
            "distribution": validators.DistributionValidator(),
            # 'downloadURL': validators.StringValidator(),
            "format": validators.StringOrListOfStringsValidator(),
            # 'hasPolicy': validators.StringValidator(),
            # 'hasVersion': validators.StringValidator(),
            # 'identifier': validators.StringValidator(),
            "isReferencedBy": validators.StringValidator(),
            # 'isVersionOf': validators.StringValidator(),
            "issued": validators.DateValidator(),
            "keyword": validators.StringOrListOfStringsValidator(),
            # 'landingPage': validators.StringValidator(),
            "language": validators.StringOrListOfStringsValidator(),
            # 'license': validators.StringValidator(),
            # 'mediaType': validators.StringValidator(),
            "modified": validators.DateValidator(),
            # 'packageFormat': validators.StringValidator(),
            "page": validators.StringValidator(),
            # 'provenance': validators.StringValidator(),
            "publisher": validators.ContactValidator(),
            # 'qualifiedAttributionwasGeneratedBy': validators.StringValidator(),
            # 'qualifiedRelation': validators.StringValidator(),
            # 'relation': validators.StringValidator(),
            # 'rights': validators.StringValidator(),
            # 'sample': validators.StringValidator(),
            # 'source': validators.StringValidator(),
            # 'spatial': validators.StringValidator(),
            "spatialResolutionInMeters": validators.IntValidator(),
            # 'status': validators.StringValidator(),
            'temporal': validators.TemporalValidator(),
            # 'temporalResolution': validators.StringValidator(),
            "theme": validators.StringOrListOfStringsValidator(),
            # 'type': validators.StringValidator(),
            # 'versionInfo': validators.StringValidator(),
            # 'versionNotes': validators.StringValidator(),
        }

    def get_validator(self, key: Any) -> Validator:
        """Get validator for key."""
        return self.validators.get(key, validators.StringValidator())

    def get_properties(self) -> List:
        """Get list of all properties."""
        return [*self.mandatory, *self.recommended, *self.optional]

    def validate_content(self, errors: Dict) -> None:
        """Check if mandatory and recommended properties are included."""
        for field in self.mandatory:
            if field not in self.metadata.keys():
                errors[validation_errors.ValidationError.ERROR_MISSING_PROPERTY].append({"field": field})

        for field in self.recommended:
            if field not in self.metadata.keys():
                errors[validation_errors.ValidationError.WARNING_MISSING_RECOMMENDED_PROPERTY].append(
                    {"field": field}
                )

    def validate(self) -> List:
        """Validate."""
        errors = defaultdict(list)

        self.validate_content(errors)

        for field, value in self.metadata.items():
            if field not in self.get_properties():
                errors[validation_errors.ValidationError.ERROR_INVALID_PROPERTY].append({"field": field})

            try:
                validator = self.get_validator(field)
            except KeyError:
                errors[validation_errors.ValidationError.ERROR_INVALID_VALUE].append(
                    {"field": field, "validator": validator}
                )
            except Exception:
                errors[validation_errors.ValidationError.ERROR_OTHER].append(
                    {"field": field, "validator": validator}
                )

            try:
                validator.validate(value)
            except Exception:
                errors[validation_errors.ValidationError.ERROR_VALIDATION].append(
                    {"field": field, "validator": validator}
                )

        for key, value in errors.items():
            print(validation_errors.ValidationError().to_string(key, value))

        return errors


class Distribution(DcatModel):
    """DCAT Distribution."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(Distribution, self).__init__(metadata)

        self.mandatory = ["accessURL"]

        self.recommended = ["availability", "description", "format", "license"]

        self.optional = [
            "status",
            "accessService",
            "byteSize",
            "compressFormat",
            "downloadURL",
            "mediaType",
            "packageFormat",
            "spatialResolutionInMeters",
            "temporalResolution",
            "conformsTo",
            "issued",
            "language",
            "modified",
            "rights",
            "title",
            "page",
            "hasPolicy",
            "checksum",
        ]
