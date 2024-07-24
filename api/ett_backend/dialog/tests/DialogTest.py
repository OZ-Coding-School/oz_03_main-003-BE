import json
import uuid
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from chatroom.models import ChatRoom
from dialog.models import AIDialog, UserDialog, AIEmotionalAnalysis
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
        self.tree_emotion = TreeEmotion.objects.create(
            tree=self.tree
        )
        self.user_dialog = UserDialog.objects.create(
            user=self.user,
            chat_room=self.chat_room,
            message="Hello, my name is ASDF"
        )
        self.ai_dialog = AIDialog.objects.create(
            user_dialog=self.user_dialog,
            message="Hello, my name is ASDF"
        )
        self.ai_emotional_analysis = AIEmotionalAnalysis.objects.create(
            ai_dialog=self.ai_dialog,
            happiness=Decimal(7.5),
            anger=Decimal(2.5),
            sadness=Decimal(0.5),
            worry=Decimal(3.5),
            indifference=Decimal(0.5),
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies["access"] = self.access_token
        self.client.cookies["refresh"] = self.refresh_token
        self.url = reverse(
            "dialog",
            kwargs={"chat_room_uuid": self.chat_room_uuid}
        )

    def test_get_dialog(self):
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
