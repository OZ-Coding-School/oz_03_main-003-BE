from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from users.models import User
from django.urls import reverse
import uuid
from rest_framework import status

class GetTreeEmotionTest(APITestCase):

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
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.create_url = reverse("tree_list_create_view")
        self.emotion_url = reverse("tree_emotion_view")

    def test_get_tree_emotion_data(self):
        for i in range(9):
            self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 9)
        self.assertEqual(TreeEmotion.objects.count(), 9)

        forest = Forest.objects.prefetch_related("related_tree").filter(user=self.user).first()
        if forest:
            response = self.client.get(self.emotion_url)

            print("#" * 20)
            print("Test 1")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.fail("No forest found for the user.")

    def test_get_tree_emotion_with_query_params(self):
        for i in range(9):
            self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 9)
        self.assertEqual(TreeEmotion.objects.count(), 9)

        forest = Forest.objects.prefetch_related("related_tree").filter(user=self.user).first()
        if forest:
            response = self.client.get(
                self.emotion_url,
                data={"detail_sentiment": ['a', 'w']}
            )

            print("#" * 20)
            print("Test 2")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.fail("No forest found for the user.")

    def test_get_tree_emotion_with_tree_uuid(self):
        self.client.post(self.create_url)
        tree_uuid = TreeDetail.objects.select_related("forest").get(forest=self.forest).tree_uuid
        response = self.client.get(
            self.emotion_url,
            data={"tree_uuid": tree_uuid, "detail_sentiment": ['a', 'w']}
        )

        print("#" * 20)
        print("Test 3")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
