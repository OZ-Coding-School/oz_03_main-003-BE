import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from dialog.models import AIDialog, AIEmotionalAnalysis, UserDialog
from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from users.models import User


class GetTreeEmotionTest(APITestCase):

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
        self.create_url = reverse("tree_create_view")
        self.emotion_list_url = reverse("tree_emotion_list_view")

    def test_get_tree_emotion_list(self):
        for i in range(9):
            self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 9)
        self.assertEqual(TreeEmotion.objects.count(), 9)

        response = self.client.get(self.emotion_list_url)

        print("#" * 50)
        print("Test 1-1")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_treedata_if_there_is_no_tree(self):
        response = self.client.get(self.emotion_list_url)
        print("#" * 50)
        print("Test 1-2")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tree_emotion_list_with_query_params(self):
        for i in range(9):
            self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 9)
        self.assertEqual(TreeEmotion.objects.count(), 9)

        forest = Forest.objects.prefetch_related("related_tree").filter(user=self.user).first()
        if forest:
            response = self.client.get(self.emotion_list_url, data={"detail_sentiment": ["a", "w"]})

            print("#" * 20)
            print("Test 2")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.fail("No forest found for the user.")

    def test_get_tree_emotion_retrieve(self):
        response = self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 1)
        self.assertEqual(TreeEmotion.objects.count(), 1)
        self.emotion_retrieve_url = reverse(
            "tree_emotion_retrieve_update_view", kwargs={"tree_uuid": response.data["tree_uuid"]}
        )
        response = self.client.get(self.emotion_retrieve_url)

        print("#" * 20)
        print("Test 3")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tree_emotion_retrieve_with_query_params(self):
        response = self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 1)
        self.assertEqual(TreeEmotion.objects.count(), 1)
        self.emotion_retrieve_url = reverse(
            "tree_emotion_retrieve_update_view", kwargs={"tree_uuid": response.data["tree_uuid"]}
        )
        response = self.client.get(self.emotion_retrieve_url, data={"detail_sentiment": ["h", "s"]})

        print("#" * 50)
        print("Test 4-1")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.emotion_retrieve_url, data={"detail_sentiment": ["h", "s", "a", "w", "i"]})

        print("#" * 50)
        print("Test 4-2")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tree_emotion_update(self):
        response = self.client.post(self.create_url)
        self.assertEqual(TreeDetail.objects.count(), 1)
        self.assertEqual(TreeEmotion.objects.count(), 1)

        tree = TreeDetail.objects.filter(tree_uuid=response.data.get("tree_uuid")).first()
        self.chat_room = ChatRoom.objects.create(user=self.user, tree=tree)
        self.user_dialog = UserDialog.objects.create(
            user=self.user, chat_room=self.chat_room, message="test user message"
        )
        self.ai_dialog = AIDialog.objects.create(user_dialog=self.user_dialog, message="test message")
        self.ai_emotional_analysis = AIEmotionalAnalysis.objects.create(
            ai_dialog=self.ai_dialog, happiness=4.8, anger=5.0, sadness=1.0, worry=0.0, indifference=8.0
        )

        self.emotion_update_url = reverse(
            "tree_emotion_retrieve_update_view", kwargs={"tree_uuid": response.data["tree_uuid"]}
        )
        response = self.client.patch(
            self.emotion_update_url,
            data={
                "message_uuid": self.ai_dialog.message_uuid,
            },
        )
        tree_emotion = TreeEmotion.objects.filter(tree=tree).first()

        print("#" * 50)
        print("Test 5")
        print(response.data)
        print("Before emotion update: ", self.ai_dialog.applied_state)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(tree_emotion.happiness), 4.8)
        self.ai_dialog.refresh_from_db()
        print("After emotion update: ", self.ai_dialog.applied_state)
        self.assertEqual(self.ai_dialog.applied_state, True)

        # 동일한 내용으로 다시 시도하면 400 출력해야함
        # self.emotion_update_url = reverse("tree_emotion_retrieve_update_view", kwargs={"tree_uuid": tree.tree_uuid})
        # response = self.client.patch(
        #     self.emotion_update_url,
        #     data={
        #         "chat_room_uuid": self.chat_room.chat_room_uuid,
        #         "happiness": 11.0,
        #     },
        # )
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
