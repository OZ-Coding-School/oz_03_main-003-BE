import uuid

from django.db import models

from common.models import TimeStampModel
from users.models import User


class Forest(TimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    forest_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    forest_level = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "forest"
