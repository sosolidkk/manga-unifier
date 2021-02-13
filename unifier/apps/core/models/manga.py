from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.support.utils import parse_url_as_image_tag


class Manga(StandardModelMixin):
    title = models.CharField(blank=False, null=False, max_length=256, verbose_name="Manga title")
    year = models.PositiveIntegerField(blank=False, null=False, verbose_name="Launch year")
    chapters_count = models.PositiveIntegerField(blank=False, null=False, default=0, verbose_name="Chapters count")
    author = models.CharField(blank=True, null=True, max_length=128, verbose_name="Author name")
    description = models.CharField(blank=True, null=True, max_length=128, verbose_name="Manga description")
    rate = models.DecimalField(blank=True, null=True, max_digits=2, decimal_places=2, verbose_name="Manga rate")
    cover = models.URLField(blank=True, null=True, max_length=128, verbose_name="Cover URL")

    def cover_tag(self):
        return parse_url_as_image_tag(self.cover)
