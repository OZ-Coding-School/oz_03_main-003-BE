import uuid

from django.db import models

from common.models import TimeStampModel
from users.models import User


class UserDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey("chatroom.ChatRoom", on_delete=models.CASCADE, null=True)
    text = models.TextField()


class AIDialog(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey("chatroom.ChatRoom", on_delete=models.CASCADE, null=True)
    user_dialog = models.OneToOneField(UserDialog, on_delete=models.CASCADE)  # 어떤 user의 질문에 대한 답변인지
    text = models.TextField()
