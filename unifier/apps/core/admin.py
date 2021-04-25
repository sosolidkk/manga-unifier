from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from unifier.apps.core.models import Favorite, Manga, MangaChapter, Novel, NovelChapter, Platform, get_user_model


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"

    list_filter = ["user", "content_type", "action_flag"]
    search_fields = ["object_repr", "change_message"]
    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = "<a href='%s'>%s</a>" % (
                reverse("admin:%s_%s_change" % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


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
        "get_manga_title",
    )
    list_filter = (
        "manga__title",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "manga__title",
    )

    def get_manga_title(self, obj):
        return obj.manga.title

    get_manga_title.admin_order_field = "manga"
    get_manga_title.short_description = "Manga Title"


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


class FavoriteInline(admin.StackedInline):
    model = Favorite
    can_delete = False
    verbose_name_plural = "favorites"


class UserAdmin(BaseUserAdmin):
    inlines = (FavoriteInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
