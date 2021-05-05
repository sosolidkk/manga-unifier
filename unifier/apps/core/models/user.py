from django.db import models
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models import Manga, Novel, get_user_model


class Favorite(StandardModelMixin):
    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    mangas = models.ManyToManyField(Manga, blank=True, related_name="favorite")
    novels = models.ManyToManyField(Novel, blank=True, related_name="favorite")

    def __str__(self):
        return f"<Favorite>: {self.user.username}"
