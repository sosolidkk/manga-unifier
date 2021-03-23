from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase
from tests.factories.user import UserFactory
from unifier.apps.core.models import User


class UserCreateAPIViewTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.payload = {
            "username": "test-user",
            "email": "test-user@email.com",
            "password": "Asdf123!",
        }

    def test_create_user_successful(self):
        response = self.client.post(reverse("create-user"), data=self.payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert 1 == User.objects.count()
        assert 1 == Token.objects.count()

        assert response.json()["username"] == User.objects.first().username
        assert response.json()["email"] == User.objects.first().email
        assert response.json()["token"] == User.objects.first().auth_token.key

    def test_create_user_with_missing_param(self):
        del self.payload["password"]
        response = self.client.post(reverse("create-user"), data=self.payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["password"] == ["This field is required."]

    def test_create_user_with_same_username(self):
        self.client.post(reverse("create-user"), data=self.payload)
        response = self.client.post(reverse("create-user"), data=self.payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 1 == User.objects.count()
        assert response.json()["username"] == ["A user with that username already exists."]


class UserDestroyAPIViewTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory.create()
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_destroy_user_successful(self):
        response = self.client.delete(reverse("delete-user"))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 0 == User.objects.count()

    def test_destroy_user_without_authorization(self):
        self.client.credentials()
        response = self.client.delete(reverse("delete-user"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Authentication credentials were not provided."

    def test_destroy_user_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 1")
        response = self.client.delete(reverse("delete-user"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid token."
