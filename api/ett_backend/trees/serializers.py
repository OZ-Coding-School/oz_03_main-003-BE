from trees.models import TreeEmotion, TreeDetail
from rest_framework import serializers


class TreeEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeEmotion
        fields = ['happiness', 'anger', 'sadness', 'worry', 'indifference']


class FilteredTreeEmotionSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(source='tree.tree_uuid')
    emotions = serializers.SerializerMethodField()

    class Meta:
        model = TreeEmotion
        fields = ['tree_uuid', 'emotions']

    def get_emotions(self, obj):
        request = self.context.get('request')
        detail_sentiments = request.query_params.getlist('detail_sentiment')

        emotions = {
            'h': 'happiness',
            'a': 'anger',
            's': 'sadness',
            'w': 'worry',
            'i': 'indifference'
        }

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
        fields = ['tree_uuid', 'tree_name', 'tree_level', 'location']


class TreeUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if "tree_level" in attrs and attrs["tree_level"] < 0:
            raise serializers.ValidationError("tree_level must be greater than or equal to 0")
        if "location" in attrs and attrs["location"] < 0:
            raise serializers.ValidationError("location must be greater than or equal to 0")
        return attrs

    class Meta:
        model = TreeDetail
        fields = ['tree_name', 'tree_level', 'location']
        extra_kwargs = {
            'tree_name': {'required': False},
            'tree_level': {'required': False},
            'location': {'required': False},
        }


class TreeEmotionListSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(source='tree.tree_uuid')
    emotions = TreeEmotionSerializer(source='*')

    class Meta:
        model = TreeEmotion
        fields = ['tree_uuid', 'emotions']