from rest_framework import serializers

from dialog.models import AIDialog, AIEmotionalAnalysis, UserDialog


class AIEmotionalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIEmotionalAnalysis
        fields = ["happiness", "anger", "sadness", "worry", "indifference"]


class AIMessageSerializer(serializers.ModelSerializer):
    message_uuid = serializers.UUIDField(read_only=True)
    sentiments = AIEmotionalAnalysisSerializer(source="aiemotionalanalysis", read_only=True)
    applied_state = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        if "message" not in attrs:
            return serializers.ValidationError("messages is required")
        if "message" in attrs and attrs["message"] == "":
            return serializers.ValidationError("messages must not empty")

        return attrs

    class Meta:
        model = AIDialog
        fields = ["sentiments", "message_uuid", "message", "applied_state"]


class AIAppliedStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDialog
        fields = ["applied_state"]


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


class DialogSerializer(serializers.Serializer):
    user = UserMessageSerializer(source="userdialog", read_only=True)
    ai = AIMessageSerializer(source="aidialog", read_only=True)

    class Meta:
        fields = ["user", "ai"]
