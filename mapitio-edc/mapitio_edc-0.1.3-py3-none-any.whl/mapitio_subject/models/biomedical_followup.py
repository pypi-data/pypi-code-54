from edc_model.models.base_uuid_model import BaseUuidModel

from .model_mixins import BiomedicalModelMixin, CrfModelMixin


class BiomedicalFollowup(CrfModelMixin, BiomedicalModelMixin, BaseUuidModel):
    class Meta(CrfModelMixin.Meta):
        verbose_name = "Biomedical Followup"
        verbose_name_plural = "Biomedical Followup"
