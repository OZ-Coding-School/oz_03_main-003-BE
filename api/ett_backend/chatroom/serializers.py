import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chatroom.models import ChatRoom
from users.models import User


class ChatRoomCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if "chat_room_name" not in attrs:
            return serializers.ValidationError("chat_room_name is required")
        if "analyze_target_name" not in attrs:
            return serializers.ValidationError("analyze_target_name is required")
        if "analyze_target_relation" not in attrs:
            return serializers.ValidationError("analyze_target_relation is required")
        return attrs

    class Meta:
        model = ChatRoom
        fields = [
            "chat_room_uuid",
            "chat_room_name",
            "analyze_target_name",
            "analyze_target_relation",
        ]


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            "chat_room_uuid",
            "chat_room_name",
            "analyze_target_name",
            "analyze_target_relation",
        ]


class ChatRoomUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if "chat_room_name" in attrs and attrs["chat_room_name"] == "":
            return serializers.ValidationError("chat_room_name must not empty")
        if "analyze_target_name" in attrs and attrs["analyze_target_name"] == "":
            return serializers.ValidationError("analyze_target_name must not empty")
        if "analyze_target_relation" in attrs and attrs["analyze_target_relation"] == "":
            return serializers.ValidationError("analyze_target_relation must not empty")
        return attrs

    def update(self, instance, validated_data):
        instance.chat_room_name = validated_data.get("chat_room_name", instance.chat_room_name)
        instance.analyze_target_name = validated_data.get("analyze_target_name", instance.analyze_target_name)
        instance.analyze_target_relation = validated_data.get(
            "analyze_target_relation", instance.analyze_target_relation
        )
        instance.save()  # 아직 실제 DB에 반영 X
        return instance

    class Meta:
        model = ChatRoom
        fields = [
            "chat_room_name",
            "analyze_target_name",
            "analyze_target_relation",
        ]
        extra_kwargs = {
            "chat_room_name": {"required": False},
            "analyze_target_name": {"required": False},
            "analyze_target_relation": {"required": False},
        }
