import logging

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from django.core.management.base import BaseCommand
from requests.models import Response
from rest_framework import status
from unifier.apps.core.models import Manga, MangaChapter, Platform
from unifier.apps.core.models.chapter import Language
from unifier.apps.core.services import BulkCreateMangaChapterService


class Command(BaseCommand):
    help = ""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        )
    }

    def handle(self, *args, **kwargs):
        self.platform = Platform.objects.get(name="neoxscan")
        mangas = self.platform.mangas.all()

        if self.platform:
            for manga in mangas:
                self.stdout.write(f"Current manga: {manga}")

                chapters_content = []

                manga_url = self._get_manga_url(manga)
                manga_id = int(self._get_manga_id(manga_url))
                chapters = self._get_manga_chapters(manga_id)
                chapters.reverse()

                if self._has_new_chapter(int(chapters[-1].find("a").text.strip().replace("Cap. ", "")), manga):
                    for chapter in chapters:
                        if not self._has_new_chapter(int(chapter.find("a").text.strip().replace("Cap. ", "")), manga):
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

                    BulkCreateMangaChapterService(
                        [MangaChapter(**{**chapter, "manga": manga}) for chapter in chapters_content]
                    ).execute()
                else:
                    self.stdout.write(f"{manga} don't have any new chapters")

    def _has_new_chapter(self, chapter_number: int, manga: Manga) -> bool:
        last_chapter = manga.manga_chapters.last().number if manga.manga_chapters.last() else None
        if last_chapter:
            if chapter_number == last_chapter:
                return False
        return True

    def _is_valid_response(self, response: Response) -> bool:
        if response.status_code == status.HTTP_200_OK:
            return True
        return False

    def _get_manga_url(self, manga: Manga) -> str:
        print("--> Getting manga url")

        title = ""
        if manga.title == "The Beginning After The End":
            title = "O começo depois do fim"
        else:
            title = manga.title

        payload = {"action": "wp-manga-search-manga", "title": title}
        response = requests.post(self.platform.url_search, data=payload, headers=self.headers)

        _data = response.json().get("data", None)
        if _data is not None:
            manga_url = _data[0].get("url", None)
            return manga_url

    def _get_manga_id(self, manga_url: str) -> str:
        print("--> Getting manga id")

        delimiter = "?p="

        response = requests.get(manga_url)
        soup = BeautifulSoup(response.text, "html.parser")
        shortlink = soup.find("link", {"rel": "shortlink"}).attrs.get("href")
        index = shortlink.find(delimiter)
        id = shortlink[index:].replace(delimiter, "")

        return id

    def _get_manga_chapters(self, manga_id: int) -> ResultSet:
        print("--> Getting manga chapters")

        payload = {"action": "manga_get_chapters", "manga": manga_id}
        response = requests.post(self.platform.url_search, data=payload, headers=self.headers)
        chapters = self._parse_manga_chapters(response)

        return chapters

    def _parse_manga_chapters(self, response: Response) -> ResultSet:
        soup = BeautifulSoup(response.text, "html.parser")
        chapters = soup.find_all("li")

        return chapters

    def _get_chapter_data(self, chapter: Tag) -> dict:
        data = {}

        data["number"] = int(chapter.find("a").text.strip().replace("Cap. ", ""))
        data["title"] = chapter.find("a").text.strip()
        data["language"] = Language.PORTUGUESE_BR
        data["images_url"] = chapter.find("a").attrs.get("href")
        data["images"] = []

        return data

    def _get_chapter_images(self, chapter: dict, response: Response) -> None:
        content = BeautifulSoup(response.text, "html.parser")
        images = content.find_all("div", {"class": "page-break no-gaps"})

        for image in images:
            src = image.find("img").attrs.get("data-src").strip()
            chapter["images"].append(src)
        del chapter["images_url"]
