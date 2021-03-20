from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase
from tests.factories.chapter import MangaChapterFactory, NovelChapterFactory
from tests.factories.manga import MangaFactory
from tests.factories.novel import NovelFactory
from tests.factories.user import UserFactory


class MangaViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.manga = MangaFactory()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_manga_fields(self):
        response = self.client.get(reverse("manga-list"))

        assert status.HTTP_200_OK == response.status_code
        assert 1 == response.json()["count"]
        assert (
            "id",
            "title",
            "year",
            "chapters_count",
            "author",
            "description",
            "rate",
            "status",
            "cover",
            "tags",
            "manga_url",
        ) == tuple(response.json()["results"][0].keys())

    def test_assert_manga_detail_fields(self):
        response = self.client.get(reverse("manga-detail", args=[self.manga.id]))

        assert status.HTTP_200_OK == response.status_code
        assert (
            "id",
            "title",
            "year",
            "chapters_count",
            "author",
            "description",
            "rate",
            "status",
            "cover",
            "tags",
            "chapters",
        ) == tuple(response.json().keys())


class MangaChapterRetrieveViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.manga_chapter = MangaChapterFactory()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_manga_chapter_fields(self):
        response = self.client.get(reverse("manga-chapter-detail", args=[self.manga_chapter.id]))

        assert status.HTTP_200_OK == response.status_code
        assert ("id", "number", "title", "language", "images",) == tuple(response.json().keys())


class NovelViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.novel = NovelFactory()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_novel_fields(self):
        response = self.client.get(reverse("novel-list"))

        assert status.HTTP_200_OK == response.status_code

        assert 1 == response.json()["count"]
        assert (
            "id",
            "title",
            "year",
            "chapters_count",
            "author",
            "description",
            "rate",
            "status",
            "cover",
            "novel_url",
        ) == tuple(response.json()["results"][0].keys())

    def test_assert_novel_detail_fields(self):
        response = self.client.get(reverse("novel-detail", args=[self.novel.id]))

        assert status.HTTP_200_OK == response.status_code

        assert (
            "id",
            "title",
            "year",
            "chapters_count",
            "author",
            "description",
            "rate",
            "status",
            "cover",
            "chapters",
        ) == tuple(response.json().keys())


class NovelChapterRetrieveViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.novel_chapter = NovelChapterFactory()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_novel_chapter_fields(self):
        response = self.client.get(reverse("novel-chapter-detail", args=[self.novel_chapter.id]))

        assert status.HTTP_200_OK == response.status_code
        assert ("id", "number", "title", "language", "body",) == tuple(response.json().keys())
