from django.contrib import admin
from .models import Space


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "space_type",
        "country",
        "parent",
    )
    raw_id_fields = ("country", "parent")
