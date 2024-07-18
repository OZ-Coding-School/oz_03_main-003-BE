import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chatroom.models import ChatRoom
from dialog.models import UserDialog
from users.models import User


class UserMessageReceiveTest(TestCase):
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

    def test_message_send(self):
        response = self.client.post(
            path=reverse("user-message-send"),
            data={
                "user_uuid": self.chat_room_uuid,
                "chat_room_uuid": self.chat_room_uuid,
                "user_message": "my message 123",
            },
            format="json",
        )

        self.assertEqual(UserDialog.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
