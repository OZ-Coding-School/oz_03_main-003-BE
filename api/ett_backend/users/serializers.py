from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import User


class EmptySerializer(serializers.Serializer):
    pass


class UserTokenVerifySerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        access_token = attrs.get("access_token")

        if not access_token:
            raise serializers.ValidationError({"message": "Access token is missing"})

        try:
            # AccessToken 객체를 생성하여 토큰 검증.
            AccessToken(access_token)
        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError({"message": "Invalid access token"})

        return attrs


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
            user = get_object_or_404(User, uuid=user_uuid, is_active=True)

        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError({"message": "Invalid refresh token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User does not exist"})

        attrs["user"] = user
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

        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError({"message": "Invalid refresh token"})
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
            raise serializers.ValidationError({"message": "Invalid refresh token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User does not exist"})

        attrs["user"] = user
        return attrs
