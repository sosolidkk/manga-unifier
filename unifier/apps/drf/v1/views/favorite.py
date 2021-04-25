from uuid import UUID

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from unifier.apps.core.models import Favorite, Manga, Novel


class FavoriteApiView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        manga = Manga.objects.get_or_none(id=request.data["id"])
        novel = Novel.objects.get_or_none(id=request.data["id"])
        favorite, _ = Favorite.objects.get_or_create(user=request.user)

        if manga:
            favorite.mangas.add(manga)
        if novel:
            favorite.novels.add(novel)
        return Response({"message": "Item was added to favorites."}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        if created:
            return Response({"error": "There isn't any favorite linked to this user."}, status=status.HTTP_200_OK)

        favorite.mangas.remove(UUID(request.data["id"]))
        favorite.novels.remove(UUID(request.data["id"]))
        return Response({"message": "Item was removed from favorites."}, status=status.HTTP_200_OK)
