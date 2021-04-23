from rest_framework import serializers
from rest_framework.reverse import reverse
from unifier.apps.core.models import Manga, Novel, Platform


class MangaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ["title", "year", "chapters_count"]


class NovelPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ["title", "year", "chapters_count"]


class PlatformSerializer(serializers.ModelSerializer):
    mangas = MangaPlatformSerializer(read_only=True, many=True)
    novels = NovelPlatformSerializer(read_only=True, many=True)
    platform_url = serializers.SerializerMethodField()

    class Meta:
        model = Platform
        fields = [
            "url",
            "name",
            "url_search",
            "mangas",
            "novels",
            "platform_url",
        ]

    def get_platform_url(self, obj):
        return reverse("platform-detail", args=[obj.id])


class PlatformSerializerDetail(serializers.ModelSerializer):
    mangas = MangaPlatformSerializer(read_only=True, many=True)
    novels = NovelPlatformSerializer(read_only=True, many=True)

    class Meta:
        model = Platform
        fields = PlatformSerializer.Meta.fields[:-1]
