from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel


class AreaTemplate(TimeStampedModel):
    name = models.CharField(max_length=100)
    space = models.OneToOneField(
        "space.Space",
        on_delete=models.CASCADE,
        related_name="geo_templates"
    )
    mpoly = models.MultiPolygonField()
    wkt = models.CharField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "area_template"

    def __str__(self):
        return self.name
