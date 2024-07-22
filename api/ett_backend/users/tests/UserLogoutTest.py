import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, RefreshToken

from users.models import User


class UserLogoutTest(APITestCase):

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
        self.url = reverse("user_logout")

    def test_user_logout(self):
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token

        response = self.client.post(self.url)

        # 응답 쿠키 확인
        print("Response Cookies:", response.cookies)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(BlacklistedToken.objects.filter(token__jti=self.refresh["jti"]).exists())

        # 빈 값으로 설정된 쿠키 확인
        self.assertEqual(response.cookies["access"].value, "")
        self.assertEqual(response.cookies["refresh"].value, "")
