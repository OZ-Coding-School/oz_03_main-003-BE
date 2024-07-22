import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

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

    def test_create_chat_room(self):
        self.client.post(
            path=reverse("create_chat_room"),
            data={
                "user_uuid": self.user.uuid,
                "chat_room_name": "test",
                "analyze_target_name": "test target",
                "analyze_target_relation": "test relation",
            },
            format="json",
        )
        self.assertEqual(ChatRoom.objects.count(), 1)

        chat_room = ChatRoom.objects.get(user=self.user)
        self.assertEqual(chat_room.chat_room_name, "test")
        self.assertEqual(chat_room.analyze_target_name, "test target")
        self.assertEqual(chat_room.analyze_target_relation, "test relation")

        print(chat_room.chat_room_uuid)
        print(chat_room.chat_room_name)
        print(chat_room.analyze_target_name)
        print(chat_room.analyze_target_relation)
