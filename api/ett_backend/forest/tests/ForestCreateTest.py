from rest_framework.test import APITestCase, APIClient

import uuid

from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from forest.models import Forest
from users.models import User
from rest_framework import status


class ForestCreateTest(APITestCase):

    def setUp(self):
        # Given
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
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("forest_create")

    def test_forest_creation(self):
        # When
        response = self.client.post(path=self.url)
        print(response.data)

        # Then
        self.assertEqual(Forest.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["forest_uuid"], Forest.objects.filter(user=self.user).first().forest_uuid)
        created_forest = Forest.objects.filter(user=self.user).first()
        self.assertEqual(created_forest.user, self.user)
