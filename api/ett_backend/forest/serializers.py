from django.db import transaction
from rest_framework import serializers

from forest.models import Forest
from users.models import User

from django.shortcuts import get_object_or_404


class ForestCreateSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField()

    def validate(self, attrs):
        user = get_object_or_404(User, uuid=attrs["user_uuid"])
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            forest = Forest.objects.create(
                user = validated_data["user"],
            )
        return forest

    class Meta:
        model = Forest
        fields = ["user_uuid"]


class ForestRetreiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = ['forest_uuid', 'forest_level']


class ForestDeleteSerializer(serializers.Serializer):
    forest_uuid = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        forest = get_object_or_404(Forest, forest_uuid=attrs["forest_uuid"])
        attrs["forest"] = forest
        return attrs


