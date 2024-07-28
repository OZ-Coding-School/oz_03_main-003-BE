import uuid

from django.db import models

from chatroom.models import ChatRoom
from common.models import TimeStampModel
from users.models import User


class UserDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="user_dialog")
    # 채팅방 삭제 시 자동으로 해당 채팅방에 묶여있던 사용자 메세지 삭제 -> AI 메세지 삭제 -> AI 감정 데이터 삭제

    message_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    message = models.TextField()

    class Meta:
        db_table = "user_dialog"


class AIDialog(TimeStampModel):
    user_dialog = models.OneToOneField(
        UserDialog, on_delete=models.CASCADE, related_name="ai_dialog"
    )  # 어떤 user dialog에 대한 답변인지

    message_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    message = models.TextField(null=True)
    applied_state = models.BooleanField(
        default=False
    )  # 해당 AI 답변이 Tree에 반영되었는지 True : 반영됨, False : 반영되지 않음

    class Meta:
        db_table = "ai_dialog"


class AIEmotionalAnalysis(TimeStampModel):
    ai_dialog = models.OneToOneField(AIDialog, on_delete=models.CASCADE)

    happiness = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 행복도
    anger = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 화남
    sadness = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 슬픔
    worry = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 걱정
    indifference = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 무관심

    class Meta:
        db_table = "ai_emotional_analysis"
