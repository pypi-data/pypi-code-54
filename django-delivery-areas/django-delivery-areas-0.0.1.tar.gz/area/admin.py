from django.contrib.gis import admin
from .models import AreaTemplate


@admin.register(AreaTemplate)
class AreaTemplateAdmin(admin.GeoModelAdmin):
    list_display = (
        "id",
        "name",
        "mpoly",
        "wkt",
        "is_active",
        "created",
        "modified"
    )
    raw_fields_id = ("space")
