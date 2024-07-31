from rest_framework import serializers

from trees.models import TreeDetail, TreeEmotion
from users.models import User

MAX_EMOTION_VALUE = 999.9


class TreeEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeEmotion
        fields = ["happiness", "anger", "sadness", "worry", "indifference"]


class FilteredTreeEmotionSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(source="tree.tree_uuid")
    emotions = serializers.SerializerMethodField()

    class Meta:
        model = TreeEmotion
        fields = ["tree_uuid", "emotions"]

    def get_emotions(self, obj):
        request = self.context.get("request")
        detail_sentiments = request.query_params.getlist("detail_sentiment")

        emotions = {"h": "happiness", "a": "anger", "s": "sadness", "w": "worry", "i": "indifference"}

        filtered_emotions = {}
        for key in detail_sentiments:
            emotion_field = emotions.get(key)
            if emotion_field:
                value = getattr(obj, emotion_field)
                filtered_emotions[emotion_field] = str(value)

        return filtered_emotions


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeDetail
        fields = ["tree_uuid", "tree_name", "tree_level", "location"]


class TreeListAdminSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(source="forest.user.uuid")
    tree_detail = TreeSerializer(source="*")

    class Meta:
        model = TreeDetail
        fields = ["user_uuid", "tree_detail"]


class TreeUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if "tree_name" in attrs and attrs["tree_name"] == "":
            raise serializers.ValidationError("tree_name must not empty")
        if "tree_level" in attrs and attrs["tree_level"] < 0:
            raise serializers.ValidationError("tree_level must be greater than or equal to 0")
        if "location" in attrs and attrs["location"] < 0:
            raise serializers.ValidationError("location must be greater than or equal to 0")
        return attrs

    class Meta:
        model = TreeDetail
        fields = ["tree_name", "tree_level", "location"]
        extra_kwargs = {
            "tree_name": {"required": False},
            "tree_level": {"required": False},
            "location": {"required": False},
        }


class TreeEmotionUpdateSerializer(serializers.ModelSerializer):
    MIN_APPLY_VALUE = 3.0

    def validate(self, attrs):
        for emotion in ["happiness", "anger", "sadness", "worry", "indifference"]:
            if emotion in attrs:
                value = attrs[emotion]
                if value < 0 or value > MAX_EMOTION_VALUE:
                    raise serializers.ValidationError(
                        f"{emotion} must be greater than or equal to 0 and less than or equal to {MAX_EMOTION_VALUE}"
                    )
        return attrs

    def update(self, instance, validated_data):
        def update_emotion(_emotion, _increment):
            # 기존 값 + 새로 들어온 값 전체적으로 업데이트
            new_value = getattr(instance, _emotion) + _increment
            return min(new_value, MAX_EMOTION_VALUE)

        emotions = ["happiness", "anger", "sadness", "worry", "indifference"]

        for emotion in emotions:
            increment = validated_data.get(emotion, getattr(instance, emotion))
            # MIN_APPLY_VALUE 이상인 감정 분석 결과만 트리 감정 테이블에 반영
            if increment >= self.MIN_APPLY_VALUE:
                setattr(instance, emotion, update_emotion(emotion, increment))

        instance.save()
        return instance

    class Meta:
        model = TreeEmotion
        fields = ["happiness", "anger", "sadness", "worry", "indifference"]
        extra_kwargs = {
            "happiness": {"required": False},
            "anger": {"required": False},
            "sadness": {"required": False},
            "worry": {"required": False},
            "indifference": {"required": False},
        }


class TreeEmotionListSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(source="tree.tree_uuid")
    emotions = TreeEmotionSerializer(source="*")

    class Meta:
        model = TreeEmotion
        fields = ["tree_uuid", "emotions"]
