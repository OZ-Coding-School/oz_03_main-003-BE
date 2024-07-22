import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from users.models import User


class ChatRoomCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            uuid=uuid.uuid4(),
            username="test",
            email="test@test.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_chat_room(self):
        response = self.client.post(
            path=reverse("create_chat_room"),
            data={
                "chat_room_name": "test",
                "analyze_target_name": "test target",
                "analyze_target_relation": "test relation",
            },
            format="json",
        )

        print("#" * 20)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 1)

        chat_room = ChatRoom.objects.get(user=self.user)
        self.assertEqual(chat_room.chat_room_name, "test")
        self.assertEqual(chat_room.analyze_target_name, "test target")
        self.assertEqual(chat_room.analyze_target_relation, "test relation")
