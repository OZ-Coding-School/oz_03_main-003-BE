from rest_framework_simplejwt.tokens import RefreshToken, BlacklistedToken
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User
import uuid

class UserLogoutTest(APITestCase):

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
        self.url = reverse("user_logout")

    def test_user_logout(self):
        # When
        self.client.cookies['access'] = self.access_token
        self.client.cookies['refresh'] = self.refresh_token
        response = self.client.post(self.url)
        print(response.data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(BlacklistedToken.objects.filter(token__jti=self.refresh["jti"]).exists())
