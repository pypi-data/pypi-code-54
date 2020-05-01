from typing import Dict
from data_catalog_dcat_validator.models.dcat import DcatModel


class Dataset(DcatModel):
    """DCAT Dataset."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(Dataset, self).__init__(metadata)
        self.mandatory = ["description", "title"]

        self.recommended = [
            "contactPoint",
            "distribution",
            "keyword",
            "publisher",
            "spatial",
            "temporal",
            "theme",
        ]

        self.optional = [
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
