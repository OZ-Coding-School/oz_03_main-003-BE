from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.s3instance import S3Instance


class EmptySerializer(serializers.Serializer):
    pass


class UserTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh_token")
        if not refresh_token:
            raise serializers.ValidationError({"message": "Refresh token is missing"})

        try:
            # Verify Refresh token
            token = RefreshToken(refresh_token)
            user_uuid = token["user_uuid"]

            # Verify valid user
            get_object_or_404(User, uuid=user_uuid, is_active=True)
        except (InvalidToken, TokenError):
            raise AuthenticationFailed({"message": "Serializer : Invalid refresh token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User does not exist"})

        return attrs


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh_token")

        if not refresh_token:
            raise serializers.ValidationError({"message": "Refresh token is missing"})

        try:
            # Verify Refresh token
            token = RefreshToken(refresh_token)
            user_uuid = token["user_uuid"]

            # Verify valid user
            get_object_or_404(User, uuid=user_uuid, is_active=True)
            attrs["refresh_token"] = token
        except (InvalidToken, TokenError):
            raise AuthenticationFailed({"message": "Invalid refresh token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User does not exist"})

        return attrs


class UserDeleteSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh_token")
        email = attrs.get("email")

        if not refresh_token:
            raise serializers.ValidationError({"message": "Refresh token is missing"})
        if not email:
            raise serializers.ValidationError({"message": "Email is missing"})

        try:
            # Verify Refresh token
            token = RefreshToken(refresh_token)
            user_uuid = token["user_uuid"]
            user = get_object_or_404(User, uuid=user_uuid, email=email, is_active=True)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed({"message": "Invalid refresh token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User does not exist"})

        attrs["refresh_token"] = token
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        profile_image_file = validated_data.pop("profile_image", None)
        if profile_image_file:
            s3instance = S3Instance().get_s3_instance()
            profile_image_url = S3Instance.upload_file(s3instance, profile_image_file, instance.uuid)
            instance.profile_image = profile_image_url

        # User data update
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "email",
            "profile_image",
            "social_platform",
            "is_active",
            "is_superuser",
            "created_at",
            "updated_at",
        ]
