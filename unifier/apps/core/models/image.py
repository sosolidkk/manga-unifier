from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models.chapter import MangaChapter


class Image(StandardModelMixin):
    path = models.URLField(blank=False, null=False, max_length=128, verbose_name="Image path URL")
    url = models.URLField(blank=False, null=False, max_length=128, verbose_name="Image URL")
    manga_chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE, related_name="images")
