import uuid

from django.db import models

from common.models import TimeStampModel  # common.py의 TimeStampModel 상속
from users.models import User


class Forest(TimeStampModel):
    forest_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    forest_level = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "forest"
