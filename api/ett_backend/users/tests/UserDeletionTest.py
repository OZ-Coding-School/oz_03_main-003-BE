import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserDeletionTest(APITestCase):

    def setUp(self):
        # Given
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
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_user_deletion(self):
        # When
        url = reverse("user_delete")
        data = {"refresh_token": self.refresh_token, "email": self.user.email}
        response = self.client.delete(url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
