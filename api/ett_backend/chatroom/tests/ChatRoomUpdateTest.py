import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from chatroom.models import ChatRoom

class ChatRoomUpdateTest(TestCase):
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

    def test_update_chat_room(self):
        new_data = {
            "user_uuid": self.user.uuid,
            "chat_room_uuid": self.chat_room.chat_room_uuid,
            "new_chat_room_name": "updated name",
            "new_analyze_target_name": "updated target name",
            "new_analyze_target_relation": "updated target relation",
        }

        response = self.client.put(
            path=reverse("chat_room_update"),
            data=new_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully updated chat room.")

        self.chat_room.refresh_from_db()
        self.assertEqual(self.chat_room.chat_room_name, "updated name")
        self.assertEqual(self.chat_room.analyze_target_name, "updated target name")
        self.assertEqual(self.chat_room.analyze_target_relation, "updated target relation")

        print(response.data)
