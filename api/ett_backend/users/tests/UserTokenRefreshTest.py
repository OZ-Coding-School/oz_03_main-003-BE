from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

class UserTokenRefreshTest(APITestCase):
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
        self.refresh_token = str(self.refresh)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_refresh_jwt_tokens(self):
        url = reverse('token_refresh')
        data = {
            'refresh_token': self.refresh_token,
            'user_uuid': str(self.user.uuid)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
