from rest_framework import mixins, viewsets
from unifier.apps.core.models import Manga, MangaChapter
from unifier.apps.drf.v1.pagination import BasePagination
from unifier.apps.drf.v1.serializers import MangaChapterDetailSerializer, MangaSerializer, MangaSerializerDetail


class MangaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MangaSerializerDetail
        return MangaSerializer


class MangaChapterRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MangaChapter.objects.all()
    serializer_class = MangaChapterDetailSerializer
    pagination_class = BasePagination
