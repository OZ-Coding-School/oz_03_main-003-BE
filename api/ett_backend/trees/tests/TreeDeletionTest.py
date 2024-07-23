import uuid

from django.urls import NoReverseMatch, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from trees.models import TreeDetail
from users.models import User


class TreeDeletionTest(APITestCase):

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
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_delete_tree(self):
        # Create a tree
        response = self.client.post(path=reverse("tree_create_view"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tree_uuid = response.data["tree_uuid"]

        response = self.client.delete(path=reverse("tree_update_delete_view", kwargs={"tree_uuid": tree_uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TreeDetail.objects.filter(forest=self.forest).count(), 0)

    def test_invalid_uuid(self):
        response = self.client.post(path=reverse("tree_create_view"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tree_uuid = response.data["tree_uuid"]
        invalid_uuid = "asdf-ghjk-qwer"

        try:
            response = self.client.delete(path=reverse("tree_update_delete_view", kwargs={"tree_uuid": invalid_uuid}))
            self.assertEqual(1, 2)
        except NoReverseMatch:
            print(response.status_code)
            self.assertEqual(1, 1)

        response = self.client.delete(path=reverse("tree_update_delete_view", kwargs={"tree_uuid": tree_uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TreeDetail.objects.filter(forest=self.forest).count(), 0)
