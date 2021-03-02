import logging
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from requests.models import Response
from unifier.apps.core.models import Manga, MangaChapter, Platform
from unifier.apps.core.models.chapter import Language
from unifier.apps.core.services import BulkCreateMangaChapterService


class Command(BaseCommand):
    help = "Isekaiscan crawler command"

    def handle(self, *args, **kwargs):
        platform = Platform.objects.get(name="isekaiscan")
        mangas = platform.mangas.all()

        if platform:
            for manga in mangas:
                manga_info = {}
                chapters_content = []

                data = {"action": "manga_get_chapters", "manga": None}
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
                    )
                }

                self.stdout.write(f"Current manga: {manga}")

                response = requests.get(f"{platform.url}manga/{slugify(manga.title)}")
                response.raise_for_status()
                content = BeautifulSoup(response.text, "html.parser")
                shortlink = content.find("link", {"rel": "shortlink"}).attrs["href"]
                data["manga"] = int(shortlink.split("=")[-1])

                post_content = content.find("div", {"class": "post-content"})
                post_status = content.find("div", {"class": "post-status"})

                # 0 - Rating, 1 - Rank, 2 - Alternative, 3 - Author, 4 - Genre
                post_content_items = post_content.find_all("div", {"class": "post-content_item"})
                manga_info["author"] = post_content_items[3].find("div", {"class": "author-content"}).text.strip()
                manga_info["tags"] = (
                    post_content_items[4].find("div", {"class": "genres-content"}).text.strip().split(",")
                )

                manga_info["status"] = post_status.find("div", {"class": "summary-content"}).text.strip()

                response = requests.post(platform.url_search, data=data, headers=headers)
                response.raise_for_status()
                content = BeautifulSoup(response.text, "html.parser")
                chapters_urls = content.find_all("a", attrs={"href": True, "class": False})

                manga_info["chapters_count"] = len(chapters_urls)

                if manga.chapters_count == manga_info["chapters_count"]:
                    self.stdout.write(f"{manga} don't have any new chapters")
                    continue

                for url in chapters_urls:
                    data = {}
                    data["title"] = url.text.strip()
                    data["number"] = int(re.findall(r"\d+", url.text.strip())[0])
                    data["language"] = Language.ENGLISH_US
                    data["manga"] = manga

                    self.stdout.write(f"Chapter: {data}")

                    _url = url.attrs["href"]
                    response = requests.get(_url, headers=headers)
                    content = BeautifulSoup(response.text, "html.parser")
                    images_div = content.find("div", {"class": "reading-content"})
                    data["images"] = [image.attrs["data-src"].strip() for image in images_div.find_all("img")]
                    chapters_content.append(data)

                BulkCreateMangaChapterService([MangaChapter(**chapter) for chapter in chapters_content]).execute()
                manga.__dict__.update(**manga_info)
                manga.save()
