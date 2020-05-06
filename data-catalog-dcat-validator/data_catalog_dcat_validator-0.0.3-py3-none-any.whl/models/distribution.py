from typing import Dict
from data_catalog_dcat_validator.models.base_model import BaseModel
from data_catalog_dcat_validator.validators.integer import IntValidator


class Distribution(BaseModel):
    """DCAT Distribution."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(Distribution, self).__init__(metadata)

    @property
    def mandatory_fields(self):
        return ["accessURL"]

    @property
    def recommended_fields(self):
        return ["availability", "description", "format", "license"]

    @property
    def optional_fields(self):
        return [
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

    @property
    def validators(self):
        return {
            "byteSize": IntValidator()
        }

    def report_errors(self, errors):
        print("Distribution:")
        for key, value in errors.items():
            print(self._error_to_string(key, value))
