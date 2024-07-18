
import uuid
from django.db import models
from users.models import User
from trees.models import TreeMap
from common.models import TimeStampModel  # common.py의 TimeStampModel 상속

class Forest(TimeStampModel):
    forest_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trees = models.ManyToManyField(TreeMap, related_name='forests')
