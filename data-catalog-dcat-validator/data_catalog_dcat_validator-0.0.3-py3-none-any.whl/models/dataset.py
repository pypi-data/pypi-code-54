from data_catalog_dcat_validator.validators.temporal import TemporalValidator
from data_catalog_dcat_validator.validators.date import DateValidator
from data_catalog_dcat_validator.validators.list_of_strings import StringOrListOfStringsValidator
from data_catalog_dcat_validator.validators.distributions import DistributionValidator
from data_catalog_dcat_validator.validators.contactpoint import ContactValidator
from data_catalog_dcat_validator.validators.integer import IntValidator
from data_catalog_dcat_validator.models.base_model import BaseModel
from data_catalog_dcat_validator.validators.string import StringValidator


class DatasetModel(BaseModel):
    """DCAT Dataset."""

    @property
    def mandatory_fields(self):
        return ["description", "title"]

    @property
    def recommended_fields(self):
        return [
            "contactPoint",
            "distribution",
            "keyword",
            "publisher",
            "spatial",
            "temporal",
            "theme",
        ]

    @property
    def optional_fields(self):
        return [
            "identifier",
            "sample",
            "versionNotes",
            "landingPage",
            "spatialResolutionInMeters",
            "temporalResolution",
            "qualifiedRelation",
            "accessRights",
            "accrualPeriodicity",
            "conformsTo",
            "creator",
            "hasVersion",
            "isReferencedBy",
            "isVersionOf",
            "identifier",
            "issued",
            "language",
            "modified",
            "provenance",
            "relation",
            "source",
            "type",
            "page",
            "versionInfo",
            "qualifiedAttribution" "wasGeneratedBy",
        ]

    @property
    def validators(self):
        return {
            "accessRights": StringValidator(),
            "accessService": StringValidator(),
            "accessURL": StringValidator(),
            "accrualPeriodicity": StringValidator(),
            "availability": StringValidator(),
            "byteSize": IntValidator(),
            "checksum": StringValidator(),
            "compressFormat": StringValidator(),
            "conformsTo": StringValidator(),
            "contactPoint": ContactValidator(),
            "creator": StringValidator(),
            "distribution": DistributionValidator(),
            "downloadURL": StringValidator(),
            "format": StringOrListOfStringsValidator(),
            "hasPolicy": StringValidator(),
            "hasVersion": StringValidator(),
            "identifier": StringValidator(),
            "isReferencedBy": StringValidator(),
            "isVersionOf": StringValidator(),
            "issued": DateValidator(),
            "keyword": StringOrListOfStringsValidator(),
            "landingPage": StringValidator(),
            "language": StringOrListOfStringsValidator(),
            "license": StringValidator(),
            "mediaType": StringValidator(),
            "modified": DateValidator(),
            "packageFormat": StringValidator(),
            "page": StringValidator(),
            "provenance": StringValidator(),
            "publisher": ContactValidator(),
            "qualifiedAttributionwasGeneratedBy": StringValidator(),
            "qualifiedRelation": StringValidator(),
            "relation": StringValidator(),
            "rights": StringValidator(),
            "sample": StringValidator(),
            "source": StringValidator(),
            "spatial": StringValidator(),
            "spatialResolutionInMeters": IntValidator(),
            "status": StringValidator(),
            "temporal": TemporalValidator(),
            "temporalResolution": StringValidator(),
            "theme": StringOrListOfStringsValidator(),
            "type": StringValidator(),
            "versionInfo": StringValidator(),
            "versionNotes": StringValidator(),
        }

    def report_errors(self, errors):
        print("Dataset:")
        for key, value in errors.items():
            print(self._error_to_string(key, value))
