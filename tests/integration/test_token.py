from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase
from tests.factories.user import UserFactory


class CreateTokenForUserTest(APITransactionTestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory(password="Asdf123!")
        self.user.set_password(self.user.password)
        self.user.save()

        self.payload = {
            "username": self.user.username,
            "password": "Asdf123!",
        }
        self.invalid_payload = {
            "username": self.user.username,
            "password": self.user.password,
        }

    def test_create_token_successful(self):
        response = self.client.post(reverse("auth-token"), data=self.payload)

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.json()
        assert response.json()["token"] == Token.objects.first().key

    def test_create_token_without_user(self):
        response = self.client.post(reverse("auth-token"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["username"] == ["This field is required."]
        assert response.json()["password"] == ["This field is required."]

    def test_create_token_with_invalid_credentials(self):
        response = self.client.post(reverse("auth-token"), data=self.invalid_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"] == ["Unable to log in with provided credentials."]
