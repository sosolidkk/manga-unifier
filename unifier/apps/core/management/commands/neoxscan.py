import logging
import re

from bs4 import BeautifulSoup
from bs4.element import Tag
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from unifier.apps.core.models import Manga, MangaChapter, Platform
from unifier.apps.core.models.chapter import Language
from unifier.apps.core.services import BulkCreateMangaChapterService
from unifier.support.http import http


class Command(BaseCommand):
    help = "Neoxscan crawler command"

    def handle(self, *args, **kwargs):
        platform = Platform.objects.get(name="neoxscan")
        mangas = platform.mangas.all()

        if platform:
            for manga in mangas:
                manga_info = {}
                chapters_content = []
                payload = {"action": "manga_get_chapters", "manga": None}

                self.stdout.write(f"Current manga: {manga}")

                title = (
                    manga.title if manga.title.lower() != "the beginning after the end" else "O começo depois do fim"
                )

                response = http.get(f"{platform.url}manga/{slugify(title)}")
                content = BeautifulSoup(response.text, "html.parser")

                payload["manga"] = self._find_manga_id(content)
                manga_info = {**self._find_manga_info(content)}

                response = http.post(platform.url_search, data=payload)
                content = BeautifulSoup(response.text, "html.parser")

                chapters_urls = list(
                    reversed(content.find_all("a", attrs={"href": True, "class": False, "title": False}))
                )
                manga_info["chapters_count"] = len(chapters_urls)

                if not self._has_new_chapter(manga, manga_info["chapters_count"]):
                    self.stdout.write(f"{manga} don't have any new chapters")
                    continue

                limit = self._find_chapter_interval(manga, manga_info["chapters_count"])
                for url in chapters_urls[manga_info["chapters_count"] - limit :]:
                    data = self._find_chapter_info(url, manga)
                    self.stdout.write(f"Chapter: {data}")

                    response = http.get(data["url"])
                    content = BeautifulSoup(response.text, "html.parser")

                    data["images"] = self._find_chapter_images(content)

                    del data["url"]

                    chapters_content.append(data)

                BulkCreateMangaChapterService([MangaChapter(**chapter) for chapter in chapters_content]).execute()
                manga.__dict__.update(**manga_info)
                manga.save()

    def _has_new_chapter(self, manga: Manga, chapters_count: int) -> bool:
        current_chapters_count = MangaChapter.objects.filter(manga=manga, language=Language.PORTUGUESE_BR).count()
        if chapters_count <= current_chapters_count:
            return False
        return True

    def _find_manga_info(self, content: BeautifulSoup) -> dict:
        _manga_info = {}

        post_content = content.find("div", {"class": "post-content"})
        post_status = content.find("div", {"class": "post-status"})
        post_status_items = post_status.find_all("div", {"class": "post-content_item"})
        summary_image = content.find("div", {"class": "summary_image"})
        post_content_items = post_content.find_all("div", {"class": "post-content_item"})

        for item in post_content_items:
            if "autor" in item.text.lower():
                _manga_info["author"] = item.find("div", {"class": "author-content"}).text.strip()
            if "gênero" in item.text.lower():
                _manga_info["tags"] = item.find("div", {"class": "genres-content"}).text.strip().split(",")

        for item in post_status_items:
            if "status" in item.text.lower():
                _manga_info["status"] = item.find("div", {"class": "summary-content"}).text.strip()

        _manga_info["cover"] = summary_image.find("img").attrs["data-src"]

        return _manga_info

    def _find_manga_id(self, content: BeautifulSoup) -> int:
        shortlink = content.find("link", {"rel": "shortlink"}).attrs["href"]
        return int(shortlink.split("=")[-1])

    def _find_chapter_info(self, element: Tag, manga: Manga) -> dict:
        data = {}
        data["title"] = element.text.strip()
        data["number"] = int(re.findall(r"\d+", element.text.strip())[0])
        data["language"] = Language.PORTUGUESE_BR
        data["manga"] = manga
        data["url"] = element.attrs["href"]
        data["images"] = []

        return data

    def _find_chapter_images(self, content: BeautifulSoup) -> list:
        images_div = content.find("div", {"class": "reading-content"})
        return [image.attrs["data-src"].strip() for image in images_div.find_all("img")]

    def _find_chapter_interval(self, manga: Manga, chapters_count: int) -> int:
        current_chapters_count = MangaChapter.objects.filter(manga=manga, language=Language.PORTUGUESE_BR).count()
        if current_chapters_count == 0:
            return chapters_count
        return abs(current_chapters_count - chapters_count)
