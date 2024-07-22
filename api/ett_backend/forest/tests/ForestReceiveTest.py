import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from users.models import User


class ForestReceiveTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            uuid=uuid.uuid4(),
            social_platform="google",
            is_active=True,
        )

        self.forest = Forest.objects.create(user=self.user, forest_uuid=uuid.uuid4(), forest_level=123)

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("forest_receive")

    def test_forest_receive(self):
        # When
        response = self.client.get(path=self.url)
        print(response.data)

        # Then
        self.assertEqual(response.data["forest_uuid"], str(self.forest.forest_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
