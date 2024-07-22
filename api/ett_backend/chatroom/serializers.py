import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chatroom.models import ChatRoom
from users.models import User


class ChatRoomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = [
            "chat_room_uuid",
        ]

    def create(self, validated_data):
        chat_room_uuid = uuid.uuid4().hex
        with transaction.atomic():
            new_chatroom = ChatRoom.objects.create(
                user=self.context["user"],
                chat_room_uuid=chat_room_uuid,
                **validated_data
            )
        return new_chatroom


class ChatRoomListSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        attrs["user"] = user
        return attrs


class ChatRoomRetrieveSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
    chat_room_uuid = serializers.UUIDField()

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"])
        attrs["user"] = user
        attrs["chat_room_name"] = chat_room.chat_room_name
        attrs["analyze_target_name"] = chat_room.analyze_target_name
        attrs["analyze_target_relation"] = chat_room.analyze_target_relation
        return attrs


class ChatRoomUpdateSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)
    chat_room_uuid = serializers.UUIDField(write_only=True)
    new_chat_room_name = serializers.CharField(required=False, allow_blank=True)
    new_analyze_target_name = serializers.CharField(required=False, allow_blank=True)
    new_analyze_target_relation = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"], user=user)
        attrs["chat_room"] = chat_room
        return attrs

    def update(self, instance, validated_data):
        instance.chat_room_name = validated_data.get("new_chat_room_name", instance.chat_room_name)
        instance.analyze_target_name = validated_data.get("new_analyze_target_name", instance.analyze_target_name)
        instance.analyze_target_relation = validated_data.get(
            "new_analyze_target_relation", instance.analyze_target_relation
        )
        instance.save()
        return instance

    class Meta:
        model = ChatRoom
        fields = [
            "user_uuid",
            "chat_room_uuid",
            "new_chat_room_name",
            "new_analyze_target_name",
            "new_analyze_target_relation",
        ]


class ChatRoomDeleteSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)
    chat_room_uuid = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"], user=user)
        attrs["chat_room"] = chat_room
        return attrs

    class Meta:
        model = ChatRoom
        fields = ["user_uuid", "chat_room_uuid"]
