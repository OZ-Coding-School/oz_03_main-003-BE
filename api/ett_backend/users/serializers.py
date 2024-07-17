from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterOrLoginSerializer(serializers.Serializer):
    has_account = serializers.BooleanField(read_only=True)
    email = serializers.EmailField()
    profile_image = serializers.URLField()
    name = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()
        if user:
            attrs["user"] = user
            attrs["has_account"] = True
        else:
            attrs["has_account"] = False
        return attrs

# class UserLogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField(write_only=True)
#
#     def validate(self, attrs):
#         # Refresh 토큰을 검증하고, 블랙리스트에 넣어버린다
#         try:
#             RefreshToken(attrs["refresh"]).blacklist()
#         except Exception as e:
#             raise serializers.ValidationError("Invalid token or token already blacklisted.")
#         return attrs
#
#
# class UserDeleteSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     refresh = serializers.CharField(write_only=True)
#
#     def validate(self, attrs):
#         try:
#             user = User.objects.get(email=attrs["email"])
#             attrs["user"] = user
#         except User.DoesNotExist:
#             raise serializers.ValidationError("There is no user with this email.")
#
#         try:
#             RefreshToken(attrs["refresh"]).blacklist()
#         except Exception as e:
#             raise serializers.ValidationError("Invalid token or token already blacklisted.")
#
#         return attrs


class EmptySerializer(serializers.Serializer):
    pass
