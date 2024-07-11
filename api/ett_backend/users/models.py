import uuid

from django.db import models

from common.models import TimeStampModel


class User(TimeStampModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_image = models.URLField(max_length=255, null=True)
