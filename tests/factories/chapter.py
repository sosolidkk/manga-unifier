import factory
from tests.factories.manga import MangaFactory
from tests.factories.novel import NovelFactory
from unifier.apps.core.models import MangaChapter, NovelChapter
from unifier.apps.core.models.chapter import Language


class MangaChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MangaChapter

    number = 1
    title = "Reborn!"
    language = Language.ENGLISH_US
    manga = factory.SubFactory(MangaFactory)


class NovelChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NovelChapter

    number = 1
    title = "Reborn!"
    language = Language.PORTUGUESE_BR
    body = "Content of a novel"
    novel = factory.SubFactory(NovelFactory)
