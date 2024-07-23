from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chatroom.models import ChatRoom
from dialog.models import UserDialog


class UserMessageSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=attrs["chat_room_uuid"])
        if "message" not in attrs:
            return serializers.ValidationError("messages is required")
        if "message" in attrs and attrs["message"] == "":
            return serializers.ValidationError("messages must not empty")
        attrs["chat_room"] = chat_room
        attrs["message"] = attrs["message"]
        return attrs

    class Meta:
        model = UserDialog
        fields = ["chat_room", "message"]
