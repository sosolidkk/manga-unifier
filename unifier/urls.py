from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from unifier.apps.drf.v1.views import (
    MangaChapterCreateViewSet,
    MangaChapterRetrieveViewSet,
    MangaViewSet,
    NovelChapterRetrieveViewSet,
    NovelViewSet,
    PlatformViewSet,
    UserCreateAPIView,
    UserDeleteAPIView,
    FavoriteApiView,
)

admin.site.site_title = "Manga Unifier"
admin.site.site_header = f"{admin.site.site_title} administration"

router = DefaultRouter()
router.register("platform", PlatformViewSet)
router.register("mangas", MangaViewSet)
router.register("novels", NovelViewSet)
router.register("manga-chapter", MangaChapterRetrieveViewSet, basename="manga-chapter")
router.register("novel-chapter", NovelChapterRetrieveViewSet, basename="novel-chapter")
router.register("create-mangachapter", MangaChapterCreateViewSet, basename="create-mangachapter")

urlpatterns = [
    path("", RedirectView.as_view(url="/admin")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/auth-token/", views.obtain_auth_token, name="auth-token"),
    path("api/v1/create-user/", UserCreateAPIView.as_view(), name="create-user"),
    path("api/v1/delete-user/", UserDeleteAPIView.as_view(), name="delete-user"),
    path("api/v1/favorite/", FavoriteApiView.as_view(), name="favorite"),
    path("api/v1/", include(router.urls)),
]
