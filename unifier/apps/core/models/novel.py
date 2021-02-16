from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.support.utils import parse_url_as_image_tag


class Novel(StandardModelMixin):
    class Meta:
        verbose_name = "Novel"
        verbose_name_plural = "Novels"

    title = models.CharField(blank=False, null=False, max_length=256, verbose_name="Novel title")
    year = models.PositiveIntegerField(blank=False, null=False, verbose_name="Launch year")
    chapters_count = models.PositiveIntegerField(blank=False, null=False, default=0, verbose_name="Chapters count")
    author = models.CharField(blank=True, null=True, max_length=128, verbose_name="Author name")
    description = models.TextField(blank=True, null=True, verbose_name="Novel description")
    rate = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2, verbose_name="Novel rate")
    status = models.CharField(blank=True, null=True, max_length=128, verbose_name="Status")
    cover = models.URLField(blank=True, null=True, max_length=256, verbose_name="Cover URL")

    def __str__(self):
        return f"{self.title} - {self.year}"

    def cover_tag(self):
        return parse_url_as_image_tag(self.cover)
