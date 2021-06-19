from uuid import UUID

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from unifier.apps.core.models import Favorite, Manga, Novel
from unifier.apps.drf.v1.pagination import BasePagination
from unifier.apps.drf.v1.serializers import FavoriteSerializer


class FavoriteApiView(generics.RetrieveAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    pagination_class = BasePagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(request.user.favorite)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        manga = Manga.objects.get_or_none(id=request.data["id"])
        novel = Novel.objects.get_or_none(id=request.data["id"])
        favorite, _ = Favorite.objects.get_or_create(user=request.user)

        if manga:
            favorite.mangas.add(manga)
        if novel:
            favorite.novels.add(novel)
        return Response({"message": "Item was added to favorites"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        if created:
            favorite.delete()
            return Response(
                {"error": "There isn't any favorite linked to this user"}, status=status.HTTP_400_BAD_REQUEST
            )

        favorite.mangas.remove(UUID(request.data["id"]))
        favorite.novels.remove(UUID(request.data["id"]))
        return Response({"message": "Item was removed from favorites"}, status=status.HTTP_200_OK)
