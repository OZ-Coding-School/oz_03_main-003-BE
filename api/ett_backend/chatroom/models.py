from django.db import models
import uuid
from common.models import TimeStampModel
from users.models import User


# Create your models here.
class ChatRoom(TimeStampModel):
    chat_room_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    chat_room_name = models.CharField(max_length=255, default="My Chat Room")  # Chat Room Name
    analyze_target_name = models.CharField(max_length=255, null=True)  # 감정 분석 할 상대방 이름
    analyze_target_relation = models.CharField(max_length=255, null=True)  # 감정 분석 할 상대방과의 관계
    user = models.ForeignKey(User, on_delete=models.CASCADE)