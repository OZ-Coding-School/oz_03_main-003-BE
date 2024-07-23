import uuid

from django.db import models

from common.models import TimeStampModel
from trees.models import TreeDetail
from users.models import User


class ChatRoom(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(TreeDetail, on_delete=models.CASCADE, null=True)

    chat_room_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    chat_room_name = models.CharField(max_length=255, default="My Chat Room")  # Chat Room Name
    analyze_target_name = models.CharField(max_length=255, null=True)  # 감정 분석 할 상대방 이름

    class Meta:
        db_table = "chat_room"
