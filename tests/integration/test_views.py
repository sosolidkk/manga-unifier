import json
from uuid import UUID

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase
from tests.factories.chapter import MangaChapterFactory, NovelChapterFactory
from tests.factories.favorite import FavoriteFactory
from tests.factories.manga import MangaFactory
from tests.factories.novel import NovelFactory
from tests.factories.platform import PlatformFactory
from tests.factories.user import UserFactory
from unifier.apps.core.models import MangaChapter


class MangaViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.manga = MangaFactory.create()
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
        self.manga_chapter = MangaChapterFactory.create()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_manga_chapter_fields(self):
        response = self.client.get(reverse("manga-chapter-detail", args=[self.manga_chapter.id]))

        assert status.HTTP_200_OK == response.status_code
        assert (
            "id",
            "number",
            "title",
            "language",
            "images",
        ) == tuple(response.json().keys())


class MangaChapterCreateViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.manga = MangaFactory.create()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        self.dict_payload = {
            "number": 1,
            "title": "My dict chapter",
            "language": 0,
            "images": ["image 1"],
            "manga": self.manga.title,
        }
        self.list_payload = [
            {
                "number": 1,
                "title": "My list chapter",
                "language": 0,
                "images": ["image 1", "image 2"],
                "manga": self.manga.title,
            },
            {
                "number": 2,
                "title": "My list chapter 2",
                "language": 1,
                "images": ["image 1", "image 2", "image 3"],
                "manga": self.manga.title,
            },
        ]

    def test_create_manga_chapter_passing_dict(self):
        response = self.client.post(
            reverse("create-mangachapter-list"),
            json.dumps(self.dict_payload),
            content_type="application/json",
        )

        assert status.HTTP_201_CREATED == response.status_code
        assert 1 == MangaChapter.objects.count()

    def test_create_manga_chapter_passing_list(self):
        response = self.client.post(
            reverse("create-mangachapter-list"),
            json.dumps(self.list_payload),
            content_type="application/json",
        )

        assert status.HTTP_201_CREATED == response.status_code
        assert 2 == MangaChapter.objects.count()


class NovelViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.novel = NovelFactory.create()
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
        self.novel_chapter = NovelChapterFactory.create()
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_novel_chapter_fields(self):
        response = self.client.get(reverse("novel-chapter-detail", args=[self.novel_chapter.id]))

        assert status.HTTP_200_OK == response.status_code
        assert (
            "id",
            "number",
            "title",
            "language",
            "body",
        ) == tuple(response.json().keys())


class PlatformViewSetTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.manga = MangaFactory.create()
        self.novel = NovelFactory.create()
        self.platform = PlatformFactory(mangas=[self.manga], novels=[self.novel])
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_assert_platform_fields(self):
        response = self.client.get(reverse("platform-list"))

        platform_data = response.json()["results"]
        platform_manga_data = platform_data[0]["mangas"]
        platform_novel_data = platform_data[0]["novels"]

        assert isinstance(platform_data, list)
        assert isinstance(platform_manga_data, list)
        assert isinstance(platform_novel_data, list)

        assert ("url", "name", "url_search", "mangas", "novels", "platform_url") == tuple(platform_data[0].keys())
        assert ("id", "title", "year", "chapters_count") == tuple(platform_manga_data[0].keys())
        assert ("id", "title", "year", "chapters_count") == tuple(platform_novel_data[0].keys())

    def test_assert_platform_field_values(self):
        response = self.client.get(reverse("platform-list"))

        platform_data = response.json()["results"]
        platform_manga_data = platform_data[0]["mangas"]
        platform_novel_data = platform_data[0]["novels"]

        assert self.platform.url == platform_data[0]["url"]
        assert self.platform.name == platform_data[0]["name"]
        assert self.platform.url_search == platform_data[0]["url_search"]
        assert reverse("platform-detail", args=[self.platform.id]) == platform_data[0]["platform_url"]

        assert self.platform.mangas.first().id == UUID(platform_manga_data[0]["id"])
        assert self.platform.mangas.first().title == platform_manga_data[0]["title"]
        assert self.platform.mangas.first().year == platform_manga_data[0]["year"]
        assert self.platform.mangas.first().chapters_count == platform_manga_data[0]["chapters_count"]

        assert self.platform.novels.first().id == UUID(platform_novel_data[0]["id"])
        assert self.platform.novels.first().title == platform_novel_data[0]["title"]
        assert self.platform.novels.first().year == platform_novel_data[0]["year"]
        assert self.platform.novels.first().chapters_count == platform_novel_data[0]["chapters_count"]

    def test_assert_platform_retrieve_fields(self):
        response = self.client.get(reverse("platform-detail", args=[self.platform.id]))

        platform_data = response.json()
        platform_manga_data = platform_data["mangas"]
        platform_novel_data = platform_data["novels"]

        assert isinstance(platform_data, dict)
        assert isinstance(platform_manga_data, list)
        assert isinstance(platform_novel_data, list)

        assert ("url", "name", "url_search", "mangas", "novels") == tuple(platform_data.keys())
        assert ("id", "title", "year", "chapters_count") == tuple(platform_manga_data[0].keys())
        assert ("id", "title", "year", "chapters_count") == tuple(platform_novel_data[0].keys())

    def test_assert_platform_retrieve_field_values(self):
        response = self.client.get(reverse("platform-detail", args=[self.platform.id]))

        platform_data = response.json()
        platform_manga_data = platform_data["mangas"]
        platform_novel_data = platform_data["novels"]

        assert self.platform.url == platform_data["url"]
        assert self.platform.name == platform_data["name"]
        assert self.platform.url_search == platform_data["url_search"]

        assert self.platform.mangas.first().id == UUID(platform_manga_data[0]["id"])
        assert self.platform.mangas.first().title == platform_manga_data[0]["title"]
        assert self.platform.mangas.first().year == platform_manga_data[0]["year"]
        assert self.platform.mangas.first().chapters_count == platform_manga_data[0]["chapters_count"]

        assert self.platform.novels.first().id == UUID(platform_novel_data[0]["id"])
        assert self.platform.novels.first().title == platform_novel_data[0]["title"]
        assert self.platform.novels.first().year == platform_novel_data[0]["year"]
        assert self.platform.novels.first().chapters_count == platform_novel_data[0]["chapters_count"]


class FavoriteApiViewTest(APITransactionTestCase):
    client = APIClient()
    unset_client = APIClient()

    def setUp(self):
        self.unset_manga = MangaFactory.create()
        self.unset_user = UserFactory.create()
        self.unset_token = self.unset_user.auth_token.key
        self.unset_client.credentials(HTTP_AUTHORIZATION=f"Token {self.unset_token}")
        self.unset_payload = {"id": str(self.unset_manga.id)}

        self.manga = MangaFactory.create()
        self.manga_payload = {"id": str(self.manga.id)}

        self.novel = NovelFactory.create()
        self.novel_payload = {"id": str(self.novel.id)}

        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        self.favorite = FavoriteFactory(user=self.user, mangas=[self.manga], novels=[self.novel])

    def test_set_manga_as_favorite(self):
        response = self.client.post(
            reverse("favorite"), json.dumps(self.manga_payload), content_type="application/json"
        )

        assert status.HTTP_201_CREATED == response.status_code
        assert response.json()["message"] == "Item was added to favorites"

    def test_set_novel_as_favorite(self):
        response = self.client.post(
            reverse("favorite"), json.dumps(self.novel_payload), content_type="application/json"
        )

        assert status.HTTP_201_CREATED == response.status_code
        assert response.json()["message"] == "Item was added to favorites"

    def test_unset_manga_as_favorite(self):
        response = self.client.delete(
            reverse("favorite"), json.dumps(self.manga_payload), content_type="application/json"
        )

        assert status.HTTP_200_OK == response.status_code
        assert response.json()["message"] == "Item was removed from favorites"

    def test_unset_novel_as_favorite(self):
        response = self.client.delete(
            reverse("favorite"), json.dumps(self.novel_payload), content_type="application/json"
        )

        assert status.HTTP_200_OK == response.status_code
        assert response.json()["message"] == "Item was removed from favorites"

    def test_unset_nonexistent_favorite(self):
        response = self.unset_client.delete(
            reverse("favorite"), json.dumps(self.unset_payload), content_type="application/json"
        )

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert response.json()["error"] == "There isn't any favorite linked to this user"

    def test_retrieve_manga_and_novel_favorites(self):
        response = self.client.get(reverse("favorite"))

        assert status.HTTP_200_OK == response.status_code

        assert len(response.json()["mangas"]) == 1
        assert len(response.json()["novels"]) == 1
        assert isinstance(response.json()["mangas"], list)
        assert isinstance(response.json()["novels"], list)
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
        ) == tuple(response.json()["mangas"][0].keys())
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
        ) == tuple(response.json()["novels"][0].keys())
