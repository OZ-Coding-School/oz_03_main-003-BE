from rest_framework import serializers

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


class EmptySerializer(serializers.Serializer):
    pass
