from django.contrib import admin
from unifier.apps.core.models import Manga, MangaChapter, Novel, NovelChapter, Platform


class NovelChapterInline(admin.TabularInline):
    model = NovelChapter


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "author",
        "chapters_count",
        "rate",
        "cover_tag",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "year",
    )


@admin.register(MangaChapter)
class MangaChapterAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "title",
        "language",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = ("title",)


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "author",
        "chapters_count",
        "rate",
        "cover_tag",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "year",
    )
    search_fields = (
        "title",
        "year",
    )
    inlines = (NovelChapterInline,)


@admin.register(NovelChapter)
class NovelChapterAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "title",
        "language",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = ("title",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "name",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "name",
    )
    search_fields = ("name",)
