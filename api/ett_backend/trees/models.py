import uuid

from django.db import models

from common.models import TimeStampModel
from users.models import User


class TreeMap(TimeStampModel):
    tree_map_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tree_level = models.PositiveIntegerField(default=0)


class TreeDetail(TimeStampModel):
    tree_name = models.CharField(max_length=255, default="My Tree")
    tree_map = models.ForeignKey(TreeMap, on_delete=models.CASCADE)
    tree_growth_level = models.PositiveIntegerField(default=0)
    location_x = models.IntegerField(default=0)  # x coordinate
    location_y = models.IntegerField(default=0)  # y coordinate
    happiness = models.PositiveIntegerField(default=0)  # 행복도
    anger = models.PositiveIntegerField(default=0)  # 화남
    sadness = models.PositiveIntegerField(default=0)  # 슬픔
    pleasure = models.PositiveIntegerField(default=0)  # 기쁨
