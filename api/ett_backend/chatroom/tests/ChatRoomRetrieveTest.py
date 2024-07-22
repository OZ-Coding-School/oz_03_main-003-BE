import uuid

from django.test import TestCase
from django.urls import reverse
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

        self.chat_room = ChatRoom.objects.create(
            user=self.user,
            chat_room_uuid=uuid.uuid4(),
            chat_room_name="test",
            analyze_target_name="test target",
            analyze_target_relation="test relation",
        )

    def test_chat_list(self):
        response = self.client.get(
            path=reverse("chat_room_retrieve_update_delete", kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chat_room_name"], "test")
        self.assertEqual(response.data["analyze_target_name"], "test target")
        print(response.data)
