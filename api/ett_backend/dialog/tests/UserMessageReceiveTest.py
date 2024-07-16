from django.test import TestCase
from users.models import User
from dialog.models import ChatRoom
import uuid


class UserMessageReceiveTest(TestCase):
    def setUp(self):
        self.chat_room_uuid = uuid.uuid4().hex
        user = User.objects.create(
            uuid=self.chat_room_uuid,
            username="test",
            email="test",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False
        )

        ChatRoom.objects.create(
            chat_room_uuid=self.chat_room_uuid,
            chat_room_name="test",
            analyze_target_name="test",
            analyze_target_relation="test",
            user=user
        )

    def test_message_send(self):
        request = self.client.post(
            path="/api/chat/send",
            data={
                "user_uuid": self.chat_room_uuid,
                "chat_room_uuid": self.chat_room_uuid,
                "message": "my message 123"
            }
        )

        self.assertEqual(request.status_code, 201)
