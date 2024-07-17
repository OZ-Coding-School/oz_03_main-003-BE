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
    happiness = models.DecimalField(max_digits=2, decimal_places=1)  # 행복도
    anger = models.DecimalField(max_digits=2, decimal_places=1)  # 화남
    sadness = models.DecimalField(max_digits=2, decimal_places=1)  # 슬픔
    worry = models.DecimalField(max_digits=2, decimal_places=1)  # 걱정
    indifference = models.DecimalField(max_digits=2, decimal_places=1)  # 무관심
