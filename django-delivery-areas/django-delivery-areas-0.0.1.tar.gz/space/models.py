from django.db import models


class Space(models.Model):
    name = models.CharField(max_length=45)
    space_type = models.CharField(max_length=45)
    country = models.ForeignKey(
        "country.Country",
        on_delete=models.CASCADE,
        related_name="spaces"
    )
    parent = models.ForeignKey(
        "space.Space",
        on_delete=models.SET_NULL,
        related_name="child",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "space"

    def __str__(self):
        return self.name
