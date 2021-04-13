from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from unifier.apps.core.models import Manga, MangaChapter
from unifier.apps.drf.v1.pagination import BasePagination
from unifier.apps.drf.v1.serializers import (
    MangaChapterCreateSerializer,
    MangaChapterDetailSerializer,
    MangaCreateSerializer,
    MangaSerializer,
    MangaSerializerDetail,
)


class MangaViewSet(viewsets.ModelViewSet):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer
    pagination_class = BasePagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MangaSerializerDetail
        if self.action in ("create", "update", "partial_update"):
            return MangaCreateSerializer
        return MangaSerializer


class MangaChapterRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MangaChapter.objects.all()
    serializer_class = MangaChapterDetailSerializer
    pagination_class = BasePagination
    permission_classes = (IsAuthenticated,)


class MangaChapterCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MangaChapter.objects.all()
    serializer_class = MangaChapterCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data),
        )
