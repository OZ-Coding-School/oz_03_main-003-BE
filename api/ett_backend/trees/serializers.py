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
    emotions = TreeEmotionSerializer(source='treeemotion') # TreeEmotion도 포함해서 응답을 나타내기 위해 설정
    # 즉, TreeDetail 모델에서 TreeEmotion 모델을 참조한다.
    # source='treeemotion'는 TreeDetail의 treeemotion 필드를 역참조 하게 된다. (FK가 TreeEmotion에 걸려 있으니까)

    class Meta:
        model = TreeDetail
        fields = ['tree_uuid', 'tree_name', 'tree_level', 'location', 'emotions']


class TreeEmotionListSerializer(serializers.ModelSerializer):
    tree_uuid = serializers.UUIDField(source='tree.tree_uuid')
    emotions = TreeEmotionSerializer(source='*')

    class Meta:
        model = TreeEmotion
        fields = ['tree_uuid', 'emotions']