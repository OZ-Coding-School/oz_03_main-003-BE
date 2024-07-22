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
            chat_room_uuid=uuid.uuid4(),
            chat_room_name="test",
            analyze_target_name="test target",
            analyze_target_relation="test relation",
        )

    def test_put_chat_room(self):
        new_data = {
            "chat_room_name": "updated name",
            "analyze_target_name": "updated target name",
            "analyze_target_relation": "updated target relation",
        }
        response = self.client.put(
            path=reverse("chat_room_retrieve_update_delete", kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid}),
            data=new_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chat_room = ChatRoom.objects.filter(user=self.user).first()
        self.assertEqual(chat_room.chat_room_name, "updated name")
        self.assertEqual(chat_room.analyze_target_name, "updated target name")
        self.assertEqual(chat_room.analyze_target_relation, "updated target relation")

    def test_patch_chat_room(self):
        new_data = {
            "chat_room_name": "updated name",
            "analyze_target_relation": "updated target relation",
        }
        response = self.client.patch(
            path=reverse("chat_room_retrieve_update_delete", kwargs={"chat_room_uuid": self.chat_room.chat_room_uuid}),
            data=new_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chat_room = ChatRoom.objects.filter(user=self.user).first()
        self.assertEqual(chat_room.chat_room_name, "updated name")
        self.assertEqual(chat_room.analyze_target_relation, "updated target relation")
