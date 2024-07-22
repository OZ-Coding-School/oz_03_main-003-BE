from django.db import transaction
from rest_framework import serializers

from forest.models import Forest
from users.models import User

from django.shortcuts import get_object_or_404


class ForestCreateSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField()

    def validate(self, attrs):
        user_uuid = attrs["user_uuid"]
        user = get_object_or_404(User, uuid=user_uuid)
        attrs["user"] = user
        if Forest.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a forest")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            forest = Forest.objects.create(
                user=validated_data["user"],
            )
        return forest

    class Meta:
        model = Forest
        fields = ["user_uuid"]


class ForestRetreiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = ['forest_uuid', 'forest_level']


class ForestUpdateDeleteSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if "forest_level" in attrs and attrs["forest_level"] < 0:
            raise serializers.ValidationError("forest_level must be greater than or equal to 0")
        return attrs

    def update(self, instance, validated_data):
        instance.forest_level = validated_data.get('forest_level', instance.forest_level)
        instance.save()
        return instance

    class Meta:
        model = Forest
        fields = ['forest_level']
        extra_kwargs = {
            'tree_level': {'required': True},
        }
