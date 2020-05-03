from django.db import models
from urlshortener.validators import shortcode_not_allowed
from urlshortener.shortcodes import get_shortcode


# Create your models here.
class URLShortenerModel(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "active"),
        ("DEACTIVE", "deactive")
    )

    title       = models.CharField(max_length=60, null=True, blank=True)
    description = models.CharField(max_length=160, null=True, blank=True)
    image       = models.ImageField(null=True, blank=True)
    url         = models.URLField()
    slug        = models.CharField(max_length=5, unique=True, validators=[shortcode_not_allowed])
    status      = models.CharField(max_length=8, choices=STATUS_CHOICES, default="active")
    created_at  = models.DateTimeField(auto_now=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url}"

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == "":
            self.slug   = get_shortcode(5)
            self.status = "ACTIVE"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Shortener"
        verbose_name_plural = "Shorteners"
        ordering            = ["-pk"]
