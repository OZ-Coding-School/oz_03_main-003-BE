from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from forest.models import Forest
from trees.models import TreeDetail
from users.models import User
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

class TreeUpdateDeleteViewTest(APITestCase):

    def setUp(self):
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
        self.tree = TreeDetail.objects.create(
            forest=self.forest,
            tree_name="My tree",
            location=0,
            tree_uuid=uuid.uuid4().hex
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.update_delete_url = reverse("tree_update_delete_view", kwargs={'tree_uuid': self.tree.tree_uuid})

    def test_delete_tree(self):
        response = self.client.delete(self.update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TreeDetail.objects.filter(tree_uuid=self.tree.tree_uuid).exists())

    def test_delete_unauthorized(self):
        self.client.credentials()
        response = self.client.delete(self.update_delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
