import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from dialog.models import UserDialog
from users.models import User


class UserMessageRetrieveTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.chat_room_uuid = uuid.uuid4()
        self.user = User.objects.create(
            uuid=uuid.uuid4(),
            username="test",
            email="test@example.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )
        self.user2 = User.objects.create(
            uuid=uuid.uuid4(),
            username="test2",
            email="test2@example.com",
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
        self.other_user_chat_room = ChatRoom.objects.create(
            chat_room_uuid=uuid.uuid4(),
            chat_room_name="test",
            user=self.user2,
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("user_message", kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid})

        self.user_dialog = UserDialog.objects.create(
            user=self.user, chat_room=self.chat_room, message="Hello, my name is ASDF"
        )
        self.user_dialog2 = UserDialog.objects.create(
            user=self.user, chat_room=self.chat_room, message="Hello, my name is QWER"
        )

    def test_user_message_retrieve(self):
        response = self.client.get(path=self.url)
        print(response.data)
        self.assertIn("message", response.data[0])
        self.assertIn("message_uuid", response.data[1])

    def test_user_message_retrieve_failed(self):
        # 다른 사용자가 생성한 채팅방 uuid를 제공한 경우
        self.url = reverse(
            "user_message",
            kwargs={"chat_room_uuid": self.other_user_chat_room.chat_room_uuid}
        )
        response = self.client.get(path=self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
