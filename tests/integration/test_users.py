from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase
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
        assert set(response.json().items()).issubset(set(self.payload.items()))

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
