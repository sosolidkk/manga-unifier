from rest_framework import serializers
from unifier.apps.core.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "email", "password", "token")

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_token(self, obj):
        try:
            token = obj.auth_token.key
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)
            return token.key
