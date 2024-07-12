from rest_framework import serializers

from .models import AIDialog, ChatRoom, UserDialog


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class UserDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDialog
        fields = "__all__"


class AIDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDialog
        fields = "__all__"
