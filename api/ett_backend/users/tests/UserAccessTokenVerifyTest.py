from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

class UserTokenVerifyTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            uuid=uuid.uuid4().hex,
            social_platform="google",
            is_active=True
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_verify_valid_access_token(self):
        url = reverse('token_verify')
        response = self.client.get(url, {'access_token': self.access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_invalid_access_token(self):
        url = reverse('token_verify')
        response = self.client.get(url, {'access_token': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_missing_access_token(self):
        url = reverse('token_verify')
        response = self.client.get(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
