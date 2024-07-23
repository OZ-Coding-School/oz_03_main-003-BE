import uuid

from django.db import models

from common.models import TimeStampModel
from users.models import User


class UserDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.OneToOneField("chatroom.ChatRoom", on_delete=models.CASCADE, null=True)

    message_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    message = models.TextField()

    class Meta:
        db_table = "user_dialog"


class AIDialog(TimeStampModel):
    user_dialog = models.OneToOneField(UserDialog, on_delete=models.CASCADE)  # 어떤 user dialog에 대한 답변인지

    message_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    message = models.TextField(null=True)
    sentiments = models.TextField(null=True)

    class Meta:
        db_table = "ai_dialog"
