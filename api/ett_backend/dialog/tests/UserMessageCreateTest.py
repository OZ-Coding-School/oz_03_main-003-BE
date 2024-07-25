import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from dialog.models import UserDialog
from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from users.models import User


class UserMessageCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            uuid=uuid.uuid4(),
            username="test",
            email="test@example.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )
        self.chat_room = ChatRoom.objects.create(
            chat_room_uuid=uuid.uuid4(),
            chat_room_name="test",
            user=self.user,
        )
        self.forest = Forest.objects.create(
            user=self.user,
        )
        self.tree = TreeDetail.objects.create(
            forest=self.forest,
            tree_name="test",
        )
        self.tree_emotion = TreeEmotion.objects.create(tree=self.tree)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("user_message", kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid})

    def test_message_send(self):
        response = self.client.post(
            path=self.url,
            data={
                "message": "my message 123",
            },
            format="json",
        )
        print(response.data)
        self.assertEqual(UserDialog.objects.count(), 1)
        self.assertEqual(UserDialog.objects.first().message, "my message 123")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_send_failed(self):
        response = self.client.post(
            path=self.url,
            data={
                "message": "",
            },
            format="json",
        )

        self.assertEqual(UserDialog.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_messages(self):
        self.client.post(
            path=self.url,
            data={
                "message": "first message",
            },
            format="json",
        )
        self.client.post(
            path=self.url,
            data={
                "message": "second message",
            },
            format="json",
        )

        self.assertEqual(UserDialog.objects.count(), 2)
