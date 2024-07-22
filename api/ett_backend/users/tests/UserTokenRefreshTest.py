import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserTokenRefreshViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            uuid=uuid.uuid4(),
            social_platform="google",
            is_active=True,
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("token_refresh")

    def test_refresh_token_valid(self):
        # 유효한 refresh token을 사용한 테스트
        response = self.client.post(self.url)
        print(response.data)

        # SUCCESS
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ACCESS_TOKEN
        self.assertIn("access", response.cookies)
        print(f"New access token : {response.cookies["access"].value}")

        # Test api with refreshed tokens
        self.client.cookies["access"] = response.cookies["access"].value
        response = self.client.get(reverse("user_profile"))
        print("Refreshed access token result : ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
