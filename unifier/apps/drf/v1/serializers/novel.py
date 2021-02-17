from rest_framework import serializers
from rest_framework.reverse import reverse
from unifier.apps.core.models import Novel, NovelChapter


class NovelChapterSerializer(serializers.ModelSerializer):
    chapter_url = serializers.SerializerMethodField()

    class Meta:
        model = NovelChapter
        fields = ["id", "number", "title", "language", "chapter_url"]

    def get_chapter_url(self, obj):
        return reverse("novel-chapter-detail", args=[obj.id])


class NovelChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovelChapter
        fields = NovelChapterSerializer.Meta.fields[:-1] + ["body"]


class NovelSerializer(serializers.ModelSerializer):
    novel_url = serializers.SerializerMethodField()

    class Meta:
        model = Novel
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
            "novel_url",
        ]

    def get_novel_url(self, obj):
        return reverse("novel-detail", args=[obj.id])


class NovelSerializerDetail(serializers.ModelSerializer):
    chapters = NovelChapterSerializer(source="novel_chapters", many=True, read_only=True)

    class Meta:
        model = Novel
        fields = NovelSerializer.Meta.fields[:-1] + ["chapters"]
