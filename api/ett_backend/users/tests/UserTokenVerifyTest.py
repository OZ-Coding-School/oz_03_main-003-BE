import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserTokenVerifyTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            uuid=uuid.uuid4().hex,
            social_platform="google",
            is_active=True,
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.url = reverse("token_verify")

    def test_token_verify(self):
        self.client.cookies["access"] = self.access_token
        response = self.client.post(self.url)
        print(self.access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_invalid(self):
        self.client.cookies["access"] = "invalid"
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
