import uuid

from django.db import models

from common.models import TimeStampModel
from forest.models import Forest


class TreeDetail(TimeStampModel):
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, related_name="related_tree")

    tree_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    tree_name = models.CharField(max_length=255, default="My Tree")
    tree_level = models.PositiveIntegerField(default=0)
    location = models.PositiveIntegerField(default=0) # Tree location

    class Meta:
        db_table = "tree_detail"


class TreeEmotion(TimeStampModel):
    tree = models.OneToOneField(TreeDetail, on_delete=models.CASCADE)

    happiness = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # 행복도
    anger = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # 화남
    sadness = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # 슬픔
    worry = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # 걱정
    indifference = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # 무관심

    class Meta:
        db_table = "tree_emotion"
