from decimal import Decimal

from django.test import TestCase
from tests.factories.manga import MangaFactory
from tests.factories.novel import NovelFactory
from unifier.apps.core.models import Manga, MangaChapter, Novel, NovelChapter, Platform
from unifier.apps.core.models.chapter import Language
from unifier.apps.core.services import (
    CreateMangaChapterService,
    CreateMangaService,
    CreateNovelChapterService,
    CreateNovelService,
    CreatePlatformService,
)


class CreateMangaChapterServiceTest(TestCase):
    def setUp(self):
        self.manga = MangaFactory()
        self.payload = {
            "number": 1,
            "title": "Random manga title",
            "language": Language.ENGLISH_US,
            "manga": self.manga,
        }

    def test_create_manga_chapter_service_with_valid_payload(self):
        CreateMangaChapterService(self.payload).execute()

        assert 1 == MangaChapter.objects.count()

        assert 1 == MangaChapter.objects.first().number
        assert "Random manga title" == MangaChapter.objects.first().title
        assert Language.ENGLISH_US == MangaChapter.objects.first().language
        assert self.manga == MangaChapter.objects.first().manga


class CreateMangaServiceTest(TestCase):
    def setUp(self):
        self.payload = {
            "title": "Random manga",
            "year": 2021,
            "chapters_count": 100,
            "author": "Sosolidkk",
            "description": "Random description",
            "rate": Decimal(5.0),
            "status": "OnGoing",
            "cover": "https://",
        }

    def test_create_manga_service_with_valid_payload(self):
        CreateMangaService(self.payload).execute()

        assert 1 == Manga.objects.count()

        assert "Random manga" == Manga.objects.first().title
        assert 2021 == Manga.objects.first().year
        assert 100 == Manga.objects.first().chapters_count
        assert "Sosolidkk" == Manga.objects.first().author
        assert "Random description" == Manga.objects.first().description
        assert Decimal(5.0) == Manga.objects.first().rate
        assert "OnGoing" == Manga.objects.first().status
        assert "https://" == Manga.objects.first().cover


class CreateNovelChapterServiceTest(TestCase):
    def setUp(self):
        self.novel = NovelFactory()
        self.payload = {
            "number": 1,
            "title": "Random novel title",
            "language": Language.PORTUGUESE_BR,
            "body": "Random novel body content",
            "novel": self.novel,
        }

    def test_create_novel_chapter_service_with_valid_payload(self):
        CreateNovelChapterService(self.payload).execute()

        assert 1 == NovelChapter.objects.count()

        assert 1 == NovelChapter.objects.first().number
        assert "Random novel title" == NovelChapter.objects.first().title
        assert Language.PORTUGUESE_BR == NovelChapter.objects.first().language
        assert "Random novel body content" == NovelChapter.objects.first().body
        assert self.novel == NovelChapter.objects.first().novel


class CreateNovelServiceTest(TestCase):
    def setUp(self):
        self.payload = {
            "title": "Random novel",
            "year": 2021,
            "chapters_count": 100,
            "author": "Sosolidkk",
            "description": "Random description",
            "rate": Decimal(5.0),
            "status": "OnGoing",
            "cover": "https://",
        }

    def test_create_novel_service_with_valid_payload(self):
        CreateNovelService(self.payload).execute()

        assert 1 == Novel.objects.count()

        assert "Random novel" == Novel.objects.first().title
        assert 2021 == Novel.objects.first().year
        assert 100 == Novel.objects.first().chapters_count
        assert "Sosolidkk" == Novel.objects.first().author
        assert "Random description" == Novel.objects.first().description
        assert Decimal(5.0) == Novel.objects.first().rate
        assert "OnGoing" == Novel.objects.first().status
        assert "https://" == Novel.objects.first().cover


class CreatePlatformServiceTest(TestCase):
    def setUp(self):
        self.payload = {
            "url": "https://",
            "name": "Random platform",
            "url_search": "https://search",
            "mangas": [MangaFactory()],
            "novels": [NovelFactory()],
        }

    def test_create_platform_service_with_valid_payload(self):
        CreatePlatformService(self.payload).execute()

        manga = Manga.objects.first()
        novel = Novel.objects.first()

        assert 1 == Platform.objects.count()

        assert "https://" == Platform.objects.first().url
        assert "Random platform" == Platform.objects.first().name
        assert "https://search" == Platform.objects.first().url_search
        assert manga.platform.first() == Platform.objects.first()
        assert novel.platform.first() == Platform.objects.first()
