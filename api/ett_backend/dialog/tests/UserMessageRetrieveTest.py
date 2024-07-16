import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from dialog.models import UserDialog
from chatroom.models import ChatRoom


class UserMessageRetrieveTest(TestCase):
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
            is_superuser=False
        )

        self.chat_room = ChatRoom.objects.create(
            chat_room_uuid=self.chat_room_uuid,
            chat_room_name="test",
            analyze_target_name="test",
            analyze_target_relation="test",
            user=self.user
        )

        self.user_dialog = UserDialog.objects.create(
            user=self.user,
            chat_room=self.chat_room,
            text="Hello, my name is ASDF"
        )

    def test_user_message_retrieve(self):
        response = self.client.get(
            path=reverse("get_user_message"),
            data={
                "user_uuid": self.user_uuid,
                "chat_room_uuid": self.chat_room_uuid,
            },
        )

        self.assertIn("user_message", response.data)
        self.assertEqual(response.data["user_message"], "Hello, my name is ASDF")
        self.assertEqual(response.status_code, status.HTTP_200_OK)