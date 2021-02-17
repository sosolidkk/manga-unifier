from rest_framework import mixins, viewsets
from unifier.apps.core.models import Novel, NovelChapter
from unifier.apps.drf.v1.pagination import BasePagination
from unifier.apps.drf.v1.serializers import NovelChapterDetailSerializer, NovelSerializer, NovelSerializerDetail


class NovelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NovelSerializerDetail
        return NovelSerializer


class NovelChapterRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = NovelChapter.objects.all()
    serializer_class = NovelChapterDetailSerializer
    pagination_class = BasePagination
