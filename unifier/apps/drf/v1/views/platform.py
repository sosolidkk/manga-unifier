from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from unifier.apps.core.models import Platform
from unifier.apps.drf.v1.pagination import BasePagination
from unifier.apps.drf.v1.serializers import PlatformSerializer, PlatformSerializerDetail


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    pagination_class = BasePagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlatformSerializerDetail
        return PlatformSerializer
