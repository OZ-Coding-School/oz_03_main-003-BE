import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from users.models import User


class ChatRoomUpdateTest(TestCase):
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
            tree=None,
            chat_room_uuid=uuid.uuid4(),
            chat_room_name="test"
        )

    def test_delete_chat_room(self):
        response = self.client.delete(
            path=reverse(
                "chat_room_retrieve_update_delete",
                kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatRoom.objects.count(), 0)
