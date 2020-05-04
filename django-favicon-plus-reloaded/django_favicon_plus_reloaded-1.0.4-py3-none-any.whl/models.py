from io import BytesIO
import sys

from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import signals

use_sites = hasattr(settings, "SITE_ID")

if use_sites:
    from django.contrib.sites.models import Site
    from django.contrib.sites.managers import CurrentSiteManager

config = {
    'shortcut icon': [16, 32, 48, 128, 192],
    'touch-icon': [192],
    'icon': [192],
    'apple-touch-icon': [57, 72, 114, 144, 180],
    'apple-touch-icon-precomposed': [57, 72, 76, 114, 120, 144, 152, 180],
}

config = getattr(settings, 'FAVICON_CONFIG', config)

image_path = getattr(settings, "FAVICON_PATH", "favicon")


def pre_delete_image(sender, instance, **kwargs):
    instance.del_image()


class Favicon(models.Model):
    title = models.CharField(max_length=100)
    faviconImage = models.ImageField(upload_to=image_path)

    isFavicon = models.BooleanField(default=True)

    objects = models.Manager()
    on_site = objects

    if use_sites:
        site = models.ForeignKey(Site, related_name="favicon", on_delete=models.CASCADE, blank=True, null=True, default=settings.SITE_ID)

        on_site = CurrentSiteManager()

        def save(self, *args, **kwargs):
            self.site = Site.objects.get_current()
            return super(Favicon, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Favicon'
        verbose_name_plural = 'Favicons'

    def get_favicons(self):
        favicons = []
        for rel in config:
            for size in config[rel]:
                favicons.append(self.get_favicon(size, rel))
        return favicons

    def __str__(self):
        return self.faviconImage.name

    def get_absolute_url(self):
        return self.faviconImage.name

    def del_image(self):
        self.faviconImage.delete()

    def get_favicon(self, size, rel, update=False):
        """
        get or create a favicon for size, rel(attr) and uploaded favicon
        optional:
            update=True
        """
        fav, _ = FaviconImg.objects.get_or_create(
            faviconFK=self, size=size, rel=rel)
        if update and fav.faviconImage:
            fav.del_image()
        if self.faviconImage and not fav.faviconImage:
            tmp = Image.open(storage.open(self.faviconImage.name))
            tmp.thumbnail((size, size), Image.ANTIALIAS)

            tmp_io = BytesIO()
            tmp.save(tmp_io, format='PNG')
            tmp_file = InMemoryUploadedFile(tmp_io, None, f"fav-{size}s.png", 'image/png', sys.getsizeof(tmp_io), None)

            fav.faviconImage = tmp_file
            fav.save()
        return fav

    def save(self, *args, **kwargs):
        update = False

        if self.isFavicon:
            for n in Favicon.on_site.exclude(pk=self.pk):
                n.isFavicon = False
                n.save()

        super(Favicon, self).save(*args, **kwargs)

        if self.faviconImage:
            for rel in config:
                for size in config[rel]:
                    self.get_favicon(size=size, rel=rel, update=update)

        # make sure default favicon is set
        self.get_favicon(size=32, rel='shortcut icon')


class FaviconImg(models.Model):
    faviconFK = models.ForeignKey(Favicon, on_delete=models.CASCADE)
    size = models.IntegerField()
    rel = models.CharField(max_length=250, null=True)
    faviconImage = models.ImageField(upload_to=image_path)

    def del_image(self):
        self.faviconImage.delete()


signals.pre_delete.connect(pre_delete_image, sender=Favicon)
signals.pre_delete.connect(pre_delete_image, sender=FaviconImg)
