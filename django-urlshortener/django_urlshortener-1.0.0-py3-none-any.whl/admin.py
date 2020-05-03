from django.contrib import admin
from urlshortener.models import URLShortenerModel
from urlshortener.modeladmin import URLShortenerModelAdmin


# Register your models here.
admin.site.register(URLShortenerModel, URLShortenerModelAdmin)
