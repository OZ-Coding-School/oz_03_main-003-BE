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
            uuid=uuid.uuid4().hex,
            social_platform="google",
            is_active=True,
        )
        self.forest = Forest.objects.create(
            user=self.user,
            forest_uuid=uuid.uuid4().hex,
            forest_level=123
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("tree_list_create_view")

    def test_tree_list(self):
        # When
        for i in range(9):
            self.client.post(self.url)

        response = self.client.get(self.url)

        # Then
        print("#" * 20)
        print("Test 1")
        print(response.data)
        self.assertEqual(TreeDetail.objects.filter(forest=self.forest).count(), 9)
        self.assertEqual(TreeEmotion.objects.filter(tree__forest=self.forest).count(), 9)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tree_query_params(self):
        # When
        self.client.post(self.url)
        tree_uuid = TreeDetail.objects.select_related("forest").get(forest=self.forest).tree_uuid
        response = self.client.get(self.url, data={"tree_uuid": tree_uuid})

        # Then
        print("#" * 20)
        print("Test 2")
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

