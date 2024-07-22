from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from users.models import User
from django.urls import reverse
from rest_framework import status

import uuid

class ForestDeletionTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            uuid=uuid.uuid4(),
            social_platform="google",
            is_active=True,
        )

        self.forest = Forest.objects.create(
            user=self.user,
            forest_uuid=uuid.uuid4(),
            forest_level=123
        )

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.delete_url = reverse("forest_update_delete", kwargs={'forest_uuid': self.forest.forest_uuid})


    def test_forest_delete(self):
        # When
        print(self.forest.forest_uuid)
        response = self.client.delete(path=self.delete_url)

        # Then
        self.assertEqual(Forest.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
