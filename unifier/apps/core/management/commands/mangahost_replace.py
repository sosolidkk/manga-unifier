from django.core.management.base import BaseCommand
from unifier.apps.core.models import Platform


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        platform = Platform.objects.get(name="mangahost")
        mangas = platform.mangas.all()

        for manga in mangas:
            chapters = manga.manga_chapters.all()
            for chapter in chapters:
                breakpoint()
                images = chapter.images
                _images = [image.replace("filestatic1", "filestatic3") for image in images]
                chapter.images = _images
                chapter.save()
