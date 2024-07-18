import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chatroom.models import ChatRoom
from dialog.models import AIDialog, UserDialog
from users.models import User


class UserMessageListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_uuid = uuid.uuid4().hex
        self.chat_room_uuid = uuid.uuid4().hex
        self.user = User.objects.create(
            uuid=self.user_uuid,
            username="test",
            email="test@example.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )

        self.chat_room = ChatRoom.objects.create(
            chat_room_uuid=self.chat_room_uuid,
            chat_room_name="test",
            analyze_target_name="test",
            analyze_target_relation="test",
            user=self.user,
        )

        self.user_dialog = UserDialog.objects.create(
            user=self.user, chat_room=self.chat_room, text="Hello, this is a test message."
        )

        self.ai_dialog = AIDialog.objects.create(
            user=self.user, chat_room=self.chat_room, user_dialog=self.user_dialog, text="This is a mocked AI response."
        )

    def test_user_message_list(self):
        response = self.client.get(path=reverse("get_user_message_list"), data={"user_uuid": self.user_uuid})

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_message"], "Hello, this is a test message.")
        self.assertEqual(response.data[0]["ai_response"], "This is a mocked AI response.")
