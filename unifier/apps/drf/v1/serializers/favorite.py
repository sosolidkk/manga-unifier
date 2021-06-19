from rest_framework import serializers
from unifier.apps.core.models import Favorite
from unifier.apps.drf.v1.serializers.manga import MangaSerializer
from unifier.apps.drf.v1.serializers.novel import NovelSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    mangas = MangaSerializer(read_only=True, many=True)
    novels = NovelSerializer(read_only=True, many=True)

    class Meta:
        model = Favorite
        fields = ["mangas", "novels"]
