import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from common.models import TimeStampModel


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, social_platform="none", **extra_fields):
        if not email:
            raise ValueError("이메일 정보를 가져올 수 없습니다")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, social_platform=social_platform, **extra_fields)
        user.set_unusable_password()  # 일단 소셜로그인만 지원하므로 패스워드 설정 X
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("uuid", uuid.uuid4())
        extra_fields.setdefault("username", "Administrator")
        extra_fields.setdefault("social_platform", "none")

        if not email:
            raise ValueError("이메일 정보를 가져올 수 없습니다")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 관리자는 소셜로그인으로 인증하는게 아니니까 패스워드 설정
        user.save(using=self._db)
        return user


class User(TimeStampModel, AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=False, db_index=True)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=False)
    profile_image = models.URLField(max_length=255, null=True)
    social_platform = models.CharField(
        choices=[("none", "none"), ("kakao", "kakao"), ("google", "google")], max_length=255, null=False, default="none"
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
