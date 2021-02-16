import factory
from tests.factories.chapter import MangaChapterFactory
from unifier.apps.core.models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    path = ""
    url = ""
    manga_chapter = factory.SubFactory(MangaChapterFactory)
