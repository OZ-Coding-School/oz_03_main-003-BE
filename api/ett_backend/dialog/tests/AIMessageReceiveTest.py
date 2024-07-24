import json
import uuid
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from dialog.models import AIDialog, AIEmotionalAnalysis, UserDialog
from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from users.models import User


class AIMessageReceiveTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_uuid = uuid.uuid4()
        self.chat_room_uuid = uuid.uuid4()
        self.user = User.objects.create(
            uuid=self.user_uuid,
            username="test",
            email="test@example.com",
            profile_image="test",
            social_platform="none",
            is_active=True,
            is_superuser=False,
        )
        self.chat_room = ChatRoom.objects.create(
            chat_room_uuid=self.chat_room_uuid,
            chat_room_name="test",
            user=self.user,
        )
        self.forest = Forest.objects.create(
            user=self.user,
        )
        self.tree = TreeDetail.objects.create(
            forest=self.forest,
            tree_name="test",
        )
        self.tree_emotion = TreeEmotion.objects.create(tree=self.tree)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse("user_message", kwargs={"chat_room_uuid": self.chat_room_uuid})

    @patch("gemini.models.genai.GenerativeModel")
    def test_ai_response(self, MockGenerativeModel):
        # AI에 실제 요청을 하지는 않고, 다음과 같은 응답 데이터가 전달된다고 가정 (Mock)
        mock_instance = MockGenerativeModel.return_value
        mock_instance.generate_content.return_value.result.candidates[0].content.parts[0].text = json.dumps(
            {
                "sentiments": {"happiness": 7.0, "sadness": 1.0, "anger": 0.0, "worry": 0.0, "indifference": 2.0},
                "message": "Mocked AI response",
            }
        )

        # Post 요청을 통해 사용자가 메세지를 전송한것으로 가정
        post_response = self.client.post(
            path=self.url,
            data={
                "message": "James: Hello, how are you?\nJenny: I am good. What about you?\n저는 Jenny 입니다",
            },
            format="json",
        )
        self.assertEqual(post_response.status_code, 201)

        # Get 요청을 통해 AI 응답 반환
        ai_response = self.client.get(
            path=reverse("ai_message", kwargs={"chat_room_uuid": self.chat_room_uuid}),
        )
        self.assertEqual(ai_response.status_code, 200)

        # UserDialog, AIDialog, AIEmotionalAnalysis가 잘 생성되었는지 확인
        self.assertEqual(UserDialog.objects.count(), 1)
        self.assertEqual(AIDialog.objects.count(), 1)
        self.assertEqual(AIEmotionalAnalysis.objects.count(), 1)

        # Response 검증
        self.assertEqual(ai_response.data.get("message"), "Mocked AI response")

        # Convert the returned sentiments to Decimal for comparison
        returned_sentiments = ai_response.data.get("sentiments")
        expected_sentiments = {
            "happiness": Decimal("7.0"),
            "sadness": Decimal("1.0"),
            "anger": Decimal("0.0"),
            "worry": Decimal("0.0"),
            "indifference": Decimal("2.0"),
        }

        for sentiment, value in expected_sentiments.items():
            self.assertEqual(Decimal(returned_sentiments[sentiment]), value)

        self.assertEqual(ai_response.data.get("applied_state"), False)

        print(ai_response.data)
