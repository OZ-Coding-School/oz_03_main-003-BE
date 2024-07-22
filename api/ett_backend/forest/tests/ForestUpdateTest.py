from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from users.models import User
from django.urls import reverse
from rest_framework import status

import uuid

class ForestUpdateTest(APITestCase):

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
        self.update_url = reverse("forest_update_delete", kwargs={'forest_uuid': self.forest.forest_uuid})


    def test_forest_update(self):
        # When
        data = {
            "forest_level": 456
        }
        response = self.client.put(path=self.update_url, data=data, format="json")

        # Then
        self.assertEqual(Forest.objects.count(), 1)
        self.assertEqual(Forest.objects.filter(forest_level=456).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forest_update_fail(self):
        # When
        data = {
            "forest_level": -456
        }
        response = self.client.put(path=self.update_url, data=data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
