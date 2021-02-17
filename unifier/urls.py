from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from unifier.apps.drf.v1.views import (
    MangaChapterRetrieveViewSet,
    MangaViewSet,
    NovelChapterRetrieveViewSet,
    NovelViewSet,
)

admin.site.site_title = "Manga Unifier"
admin.site.site_header = f"{admin.site.site_title} administration"

router = DefaultRouter()
router.register("mangas", MangaViewSet)
router.register("novels", NovelViewSet)
router.register("manga-chapter", MangaChapterRetrieveViewSet, basename="manga-chapter")
router.register("novel-chapter", NovelChapterRetrieveViewSet, basename="novel-chapter")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
