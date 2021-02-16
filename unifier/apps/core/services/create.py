import logging

from unifier.apps.core.models import Image, Manga, MangaChapter, Novel, NovelChapter, Platform
from unifier.apps.core.services.base import Command

logger = logging.getLogger(__name__)


class CreateImageService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> Image:
        logger.info(f"Creating image: {self._payload}")
        image = Image.objects.create(**self._payload)
        return image


class CreateMangaService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> Manga:
        logger.info(f"Creating manga: {self._payload}")
        manga = Manga.objects.create(**self._payload)
        return manga


class CreateMangaChapterService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> MangaChapter:
        logger.info(f"Creating manga chapter: {self._payload}")
        manga_chapter = MangaChapter.objects.create(**self._payload)
        return manga_chapter


class CreateNovelService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> Novel:
        logger.info(f"Creating novel: {self._payload}")
        novel = Novel.objects.create(**self._payload)
        return novel


class CreateNovelChapterService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> NovelChapter:
        logger.info(f"Creating novel chapter: {self._payload}")
        novel_chapter = NovelChapter.objects.create(**self._payload)
        return novel_chapter


class CreatePlatformService(Command):
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def execute(self) -> Platform:
        mangas = self._payload.pop("mangas", None)
        novels = self._payload.pop("novels", None)

        logger.info(f"Creating platform: {self._payload}")
        platform = Platform.objects.create(**self._payload)

        if mangas is not None:
            logger.info(f"Creating mangas for platform: {platform}")
            for manga in mangas:
                platform.mangas.add(manga)

        if novels is not None:
            logger.info(f"Creating novels for platform: {platform}")
            for novel in novels:
                platform.novels.add(novel)

        return platform
