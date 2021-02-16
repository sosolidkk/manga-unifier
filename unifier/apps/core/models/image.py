from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models.chapter import MangaChapter


class Image(StandardModelMixin):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    path = models.URLField(blank=False, null=False, max_length=256, verbose_name="Image path URL")
    url = models.URLField(blank=False, null=False, max_length=256, verbose_name="Image URL")
    manga_chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.url}"
