import uuid

from django.db import models

from common.models import TimeStampModel
from trees.models import TreeDetail
from users.models import User


class ChatRoom(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 사용자 삭제 시 당연히 해당 사용자가 만든 채팅방도 같이 삭제되어야 함
    tree = models.ForeignKey(TreeDetail, on_delete=models.CASCADE, null=True)
    # 트리 삭제 시 해당 트리로 생성된 채팅방도 같이 삭제됨

    chat_room_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    chat_room_name = models.CharField(max_length=255, default="My Chat Room")  # Chat Room Name

    class Meta:
        db_table = "chat_room"
