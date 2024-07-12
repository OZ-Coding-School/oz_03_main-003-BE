import uuid

from django.db import models

from common.models import TimeStampModel


class User(TimeStampModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=False)
    profile_image = models.URLField(max_length=255, null=True)
    social_platform = models.CharField(
        choices=[("none", "none"), ("kakao", "kakao"), ("google", "google")], max_length=255, null=False, default="none"
    )
