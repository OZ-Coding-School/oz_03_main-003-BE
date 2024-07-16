from rest_framework import serializers

from dialog.models import UserDialog
from chatroom.models import ChatRoom
from users.models import User
from rest_framework.generics import get_object_or_404


class UserDialogSerializer(serializers.ModelSerializer):
    # write_only=True : Request로 들어온 input 값으로만 사용하는 필드임을 명시하는 것
    user_uuid = serializers.UUIDField(write_only=True) # 클라이언트 요청에서 사용자 UUID를 받아온다.
    chat_room_uuid = serializers.UUIDField(write_only=True) # 클라이언트 요청에서 채팅방 UUID를 받아온다.
    user_message = serializers.CharField(write_only=True) # 클라이언트 요청에서 사용자가 전송한 메시지를 받아온다.

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"])
        attrs["user"] = user
        attrs["chat_room"] = chat_room
        return attrs

    def create(self, validated_data):
        # validated_data에서 user_uuid와 chat_room_uuid를 사용하여 UserDialog Data 생성
        user_dialog = UserDialog.objects.create(
            user=validated_data["user"],
            chat_room=validated_data["chat_room"],
            text=validated_data["user_message"]
        )
        return user_dialog

    class Meta:
        model=UserDialog
        fields=["user_uuid", "chat_room_uuid", "user_message"]

class UserMessageRetrieveSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField() # 클라이언트 요청에서 사용자 UUID를 받아온다.
    chat_room_uuid = serializers.UUIDField() # 클라이언트 요청에서 채팅방 UUID를 받아온다.

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"])
        attrs["user"] = user
        attrs["chat_room"] = chat_room
        return attrs


class UserMessageListSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField() # 클라이언트 요청에서 사용자 UUID를 받아온다.

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        attrs["user"] = user
        return attrs

class AIDialogSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField() # 클라이언트 요청에서 사용자 UUID를 받아온다.
    chat_room_uuid = serializers.UUIDField() # 클라이언트 요청에서 채팅방 UUID를 받아온다.

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"])
        user_dialog = get_object_or_404(UserDialog, user=user, chat_room=chat_room)

        attrs["user"] = user
        attrs["chat_room"] = chat_room
        attrs["user_dialog"] = user_dialog

        return attrs
