import factory
from unifier.apps.core.models import Platform


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Platform

    url = "https://www.wuxiaworld.com/"
    name = "Wuxiaworld"
    url_search = "https://www.wuxiaworld.com/api/novels/search?query="

    @factory.post_generation
    def mangas(self, create, extracted):
        if not create:
            return
        if extracted:
            for manga in extracted:
                self.mangas.add(manga)

    @factory.post_generation
    def novels(self, create, extracted):
        if not create:
            return
        if extracted:
            for novel in extracted:
                self.novels.add(novel)
