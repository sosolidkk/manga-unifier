from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from unifier.apps.core.models import User
from unifier.apps.drf.v1.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
