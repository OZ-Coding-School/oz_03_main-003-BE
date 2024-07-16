from rest_framework import serializers

from .models import AIDialog, ChatRoom, UserDialog


class UserDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDialog
        fields = "__all__"
