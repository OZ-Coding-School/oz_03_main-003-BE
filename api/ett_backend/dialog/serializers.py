from rest_framework import serializers
from dialog.models import UserDialog, AIDialog, AIEmotionalAnalysis


class AIMessageSerializer(serializers.ModelSerializer):
    message_uuid = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        if "message" not in attrs:
            return serializers.ValidationError("messages is required")
        if "message" in attrs and attrs["message"] == "":
            return serializers.ValidationError("messages must not empty")

        return attrs

    class Meta:
        model = AIDialog
        fields = ["message_uuid", "message"]


class UserMessageSerializer(serializers.ModelSerializer):
    message_uuid = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        if "message" not in attrs:
            return serializers.ValidationError("messages is required")
        if "message" in attrs and attrs["message"] == "":
            return serializers.ValidationError("messages must not empty")

        return attrs

    class Meta:
        model = UserDialog
        fields = ["message_uuid", "message"]


class AIEmotionalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIEmotionalAnalysis
        fields = ["happiness", "anger", "sadness", "worry", "indifference"]


class AIMessageSerializer(serializers.ModelSerializer):
    sentiments = AIEmotionalAnalysisSerializer(source='aiemotionalanalysis', read_only=True)

    class Meta:
        model = AIDialog
        fields = ["message_uuid", "message", "sentiments", "applied_state"]


class DialogSerializer(serializers.Serializer):
    user = UserMessageSerializer(source="userdialog", read_only=True)
    ai = AIMessageSerializer(source="aidialog", read_only=True)

    class Meta:
        fields = ["user", "ai"]