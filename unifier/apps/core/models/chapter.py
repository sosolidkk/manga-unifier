from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models.manga import Manga
from unifier.apps.core.models.novel import Novel


class Language(models.IntegerChoices):
    ENGLISH_US = 0
    PORTUGUESE_BR = 1


class MangaChapter(StandardModelMixin):
    number = models.PositiveIntegerField(blank=False, null=False, verbose_name="Chapter number")
    title = models.CharField(blank=False, null=False, max_length=256, verbose_name="Chapter title")
    language = models.PositiveSmallIntegerField(
        choices=Language.choices, default=Language.PORTUGUESE_BR, verbose_name="Chapter language"
    )
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name="manga_chapters")


class NovelChapter(StandardModelMixin):
    number = models.PositiveIntegerField(blank=False, null=False, verbose_name="Chapter number")
    title = models.CharField(blank=False, null=False, max_length=256, verbose_name="Chapter title")
    language = models.PositiveSmallIntegerField(
        choices=Language.choices, default=Language.PORTUGUESE_BR, verbose_name="Chapter language"
    )
    body = models.TextField(blank=False, null=False, verbose_name="Novel content")
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name="novel_chapters")
