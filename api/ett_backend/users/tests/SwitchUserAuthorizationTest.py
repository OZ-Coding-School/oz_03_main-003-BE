import uuid

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from django.urls import reverse


class SwitchUserAuthorizationTest(APITestCase):
    def setUp(self):
        # Given
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email="admin@localhost",
            password="admin"
        )
        self.user = User.objects.create_user(
            uuid=uuid.uuid4(),
            email="user@localhost",
            password="user",
        )
        self.refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.url = reverse("switch_user_authorization", kwargs={"user_uuid": self.user.uuid})

    def test_switch_user_authorization(self):
        # When
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.put(self.url, data={"is_superuser": "True"})

        # Then
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.is_superuser, True)
