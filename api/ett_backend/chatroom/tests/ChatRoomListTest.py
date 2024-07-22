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

        chat_room_list = []
        for i in range(10):
            chat_room_list.append(
                ChatRoom.objects.create(
                    user=self.user,
                    chat_room_uuid=uuid.uuid4().hex,
                    chat_room_name=f"test{i}",
                    analyze_target_name=f"test target{i}",
                    analyze_target_relation=f"test relation{i}",
                )
            )

    def test_chat_list(self):
        response = self.client.get(path=reverse("chat_room_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)
        print("#" * 50)
        print(response.data)
