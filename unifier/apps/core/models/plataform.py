from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models.manga import Manga
from unifier.apps.core.models.novel import Novel


class Platform(StandardModelMixin):
    url = models.URLField(blank=False, null=False, max_length=128, verbose_name="Platform URL")
    name = models.CharField(blank=False, null=False, max_length=128, verbose_name="Platform Name")
    url_search = models.URLField(blank=False, null=False, max_length=128, verbose_name="Platform search URL")
    mangas = models.ManyToManyField(Manga, related_name="platform")
    novels = models.ManyToManyField(Novel, related_name="platform")
