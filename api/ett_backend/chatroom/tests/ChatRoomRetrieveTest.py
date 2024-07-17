import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse
from chatroom.models import ChatRoom

class ChatRoomCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            uuid=uuid.uuid4().hex,
            username="test",
            email="test@test.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False
        )

        self.chat_room = ChatRoom.objects.create(
            user=self.user,
            chat_room_uuid=uuid.uuid4().hex,
            chat_room_name="test",
            analyze_target_name="test target",
            analyze_target_relation="test relation",
        )

    def test_chat_list(self):
        response = self.client.get(
            path=reverse("chat_room_retrieve"),
            data={
                "user_uuid": self.user.uuid,
                "chat_room_uuid": self.chat_room.chat_room_uuid
            }
        )

        self.assertEqual(response.status_code, 200)
        print(response.data)
