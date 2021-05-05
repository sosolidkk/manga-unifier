import factory
from tests.factories.user import UserFactory
from unifier.apps.core.models import Favorite


class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(UserFactory)

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
