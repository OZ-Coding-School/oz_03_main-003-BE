from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from users.models import User
from django.urls import reverse
import uuid
from rest_framework import status
class TreeCreateTest(APITestCase):

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
        self.url = reverse("tree_list_create_view")

    def test_tree_create(self):
        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(TreeDetail.objects.filter(forest=self.forest).count(), 1)
        self.assertEqual(TreeEmotion.objects.filter(tree__forest=self.forest).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tree_create_maximum(self):
        for i in range(9):
            self.client.post(self.url)

        self.assertEqual(TreeDetail.objects.count(), 9)

        # When
        response = self.client.post(self.url)

        # Then
        self.assertEqual(TreeDetail.objects.filter(forest=self.forest).count(), 9)
        self.assertEqual(TreeEmotion.objects.filter(tree__forest=self.forest).count(), 9)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
