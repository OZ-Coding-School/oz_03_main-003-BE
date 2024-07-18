import json
import uuid
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from chatroom.models import ChatRoom
from dialog.models import AIDialog, UserDialog
from users.models import User


class AIMessageReceiveTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_uuid = uuid.uuid4().hex
        self.chat_room_uuid = uuid.uuid4().hex
        self.user = User.objects.create(
            uuid=self.user_uuid,
            username="test",
            email="test@test.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )

        self.chat_room = ChatRoom.objects.create(
            chat_room_uuid=self.chat_room_uuid,
            chat_room_name="test",
            analyze_target_name="test",
            analyze_target_relation="test",
            user=self.user,
        )

    @patch("gemini.models.genai.GenerativeModel")
    def test_ai_response(self, MockGenerativeModel):
        # AI에 실제 요청을 하지는 않고, 다음과 같은 응답 데이터가 전달된다고 가정 (Mock)
        mock_instance = MockGenerativeModel.return_value
        mock_instance.generate_content.return_value = json.dumps(
            {
                "sentiments": {"happiness": 7.0, "sadness": 1.0, "angry": 0.0, "worry": 0.0, "indifference": 2.0},
                "message": "Mocked AI response",
            }
        )

        # Post 요청을 통해 사용자가 메세지를 전송한것으로 가정
        post_response = self.client.post(
            path=reverse("user-message-send"),
            data={
                "user_uuid": self.user_uuid,
                "chat_room_uuid": self.chat_room_uuid,
                "user_message": "James: Hello, how are you?\nJenny: I am good. What about you?\n저는 Jenny 입니다",
            },
            format="json",
        )
        self.assertEqual(post_response.status_code, 201)

        # Get 요청을 통해 AI 응답 반환
        get_response = self.client.get(
            path=reverse("get_ai_generate_response"),
            data={
                "user_uuid": self.user_uuid,
                "chat_room_uuid": self.chat_room_uuid,
            },
        )

        # Then
        self.assertEqual(get_response.status_code, 200)

        # UserDialog, AIDialog가 잘 생성되었는지 확인
        self.assertEqual(UserDialog.objects.count(), 1)
        self.assertEqual(AIDialog.objects.count(), 1)

        response_data = get_response.json()
        self.assertEqual(response_data["message"], "Mocked AI response")
        self.assertEqual(
            response_data["sentiments"],
            {"happiness": 7.0, "sadness": 1.0, "angry": 0.0, "worry": 0.0, "indifference": 2.0},
        )
