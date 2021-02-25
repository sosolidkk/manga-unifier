from rest_framework import serializers
from rest_framework.reverse import reverse
from unifier.apps.core.models import Manga, MangaChapter


class MangaChapterSerializer(serializers.ModelSerializer):
    chapter_url = serializers.SerializerMethodField()

    class Meta:
        model = MangaChapter
        fields = ["id", "number", "title", "language", "chapter_url"]

    def get_chapter_url(self, obj):
        return reverse("manga-chapter-detail", args=[obj.id])


class MangaChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaChapter
        fields = MangaChapterSerializer.Meta.fields[:-1] + ["images"]


class MangaSerializer(serializers.ModelSerializer):
    manga_url = serializers.SerializerMethodField()

    class Meta:
        model = Manga
        fields = [
            "id",
            "title",
            "year",
            "chapters_count",
            "author",
            "description",
            "rate",
            "status",
            "cover",
            "manga_url",
        ]

    def get_manga_url(self, obj):
        return reverse("manga-detail", args=[obj.id])


class MangaSerializerDetail(serializers.ModelSerializer):
    chapters = MangaChapterSerializer(source="manga_chapters", many=True, read_only=True)

    class Meta:
        model = Manga
        fields = MangaSerializer.Meta.fields[:-1] + ["chapters"]
