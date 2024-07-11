import uuid

from django.db import models

from common.models import TimeStampModel
from users.models import User


class UserDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class AIDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_dialog = models.OneToOneField(UserDialog, on_delete=models.CASCADE)  # 어떤 user의 질문에 대한 답변인지
    text = models.TextField()


class ChatRoom(TimeStampModel):
    chat_room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    analyze_target_name = models.CharField(max_length=255)  # 감정 분석 할 상대방 이름
    analyze_target_relation = models.CharField(max_length=255)  # 감정 분석 할 상대방과의 관계
    user = models.ForeignKey(User, on_delete=models.CASCADE)
