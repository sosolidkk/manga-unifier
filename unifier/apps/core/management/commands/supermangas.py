import logging

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from django.core.management.base import BaseCommand
from requests.models import Response
from rest_framework import status
from unifier.apps.core.models import Manga, Platform
from unifier.apps.core.models.chapter import Language
from unifier.apps.core.services import CreateImageService, CreateMangaChapterService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Supermangas crawler command"

    def handle(self, *args, **kwargs):
        platform = Platform.objects.get(name="supermangas")
        mangas = platform.mangas.all()

        if platform:
            for manga in mangas:
                chapters_content = []

                self.stdout.write(f"Current manga: {manga}")
                query_params = {"parametro": manga.title}

                response = requests.get(platform.url_search, params=query_params)
                if not self._is_valid_response(response):
                    self.stdout.write(f"status_code: {response.status_code} | manga: {manga}")
                    continue

                manga_url = self._get_manga_url(response)

                response = requests.get(manga_url)
                if not self._is_valid_response(response):
                    self.stdout.write(f"status_code: {response.status_code} | manga: {manga}")
                    continue

                chapters = self._get_chapters_content(response)
                for chapter in chapters:
                    if not self._has_new_chapter(int(chapter.find("span").text), manga):
                        self.stdout.write(f"{manga} don't have any new chapters")
                        break

                    data = self._get_chapter_data(chapter)
                    self.stdout.write(f"chapter: {data}")
                    chapters_content.append(data)

                for chapter in chapters_content:
                    response = requests.get(chapter["images_url"])
                    if not self._is_valid_response(response):
                        self.stdout.write(f"status_code: {response.status_code} | manga: {manga}")

                    self._get_chapter_images(chapter, response)
                    self.stdout.write(f"Images for chapter {chapter['number']}")

                for chapter in chapters_content:
                    images = chapter.pop("images")
                    manga_chapter = CreateMangaChapterService({**chapter, "manga": manga}).execute()
                    for image in images:
                        CreateImageService({"url": image, "manga_chapter": manga_chapter}).execute()

    def _is_valid_response(self, response: Response) -> bool:
        if response.status_code == status.HTTP_200_OK:
            return True
        return False

    def _has_new_chapter(self, chapter_number: int, manga: Manga) -> bool:
        # This can be improved and changed to .chapters_count instead of doing a query
        last_chapter = manga.manga_chapters.last().number if manga.manga_chapters.last() else None
        if last_chapter:
            if chapter_number == last_chapter:
                return False
        return True

    def _get_manga_url(self, response: Response) -> str:
        content = BeautifulSoup(response.text, "html.parser")
        articles = content.find_all("article", {"class": "box_view list"})
        article = [article for article in articles if "manhwa" in article.text.lower()][0]
        manga_url = article.find("a").attrs.get("href")

        return manga_url

    def _get_chapters_content(self, response: Response) -> ResultSet:
        content = BeautifulSoup(response.text, "html.parser")
        chapters = content.find_all("div", {"class", "boxTop10"})
        return chapters

    def _get_chapter_data(self, chapter: Tag) -> dict:
        data = {}
        data["number"] = chapter.find("span").text
        data["title"] = chapter.find("a").text.strip()
        data["images_url"] = chapter.find("a").attrs.get("href")
        data["language"] = Language.PORTUGUESE_BR
        data["images"] = []

        return data

    def _get_chapter_images(self, chapter: dict, response: Response) -> None:
        content = BeautifulSoup(response.text, "html.parser")
        images = content.find_all("div", {"class": "capituloViewBox"})

        for image in images:
            src = image.find("img").attrs.get("data-src")
            chapter["images"].append(src)
        del chapter["images_url"]
