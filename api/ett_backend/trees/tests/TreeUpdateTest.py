from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from forest.models import Forest
from trees.models import TreeDetail
from users.models import User
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

class TreeUpdateViewTest(APITestCase):

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
        self.tree = TreeDetail.objects.create(
            forest=self.forest,
            tree_name="My tree",
            location=0,
            tree_uuid=uuid.uuid4()
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.update_url = reverse("tree_update_delete_view", kwargs={'tree_uuid': self.tree.tree_uuid})

    def test_update_tree_name(self):
        data = {
            "tree_name": "Updated tree name",
            "tree_level": 546,
            "location": 153
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tree.refresh_from_db()
        self.assertEqual(self.tree.tree_name, "Updated tree name")

    def test_partial_update_tree_name(self):
        data = {
            "tree_name": "Partially updated tree name"
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tree.refresh_from_db()
        self.assertEqual(self.tree.tree_name, "Partially updated tree name")

    def test_update_tree_level(self):
        data = {
            "tree_level": 456
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tree_level_fail(self):
        data = {
            "tree_level": -435
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_tree_location(self):
        data = {
            "location": 565
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tree_location_fail(self):
        data = {
            "location": -153
        }
        response = self.client.put(path=self.update_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
