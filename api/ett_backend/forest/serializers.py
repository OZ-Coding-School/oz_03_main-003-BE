from rest_framework import serializers

from trees.models import TreeMap

from .models import Forest


class TreeMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeMap
        fields = "__all__"


class ForestSerializer(serializers.ModelSerializer):
    trees = TreeMapSerializer(many=True, read_only=True)

    class Meta:
        model = Forest
        fields = "__all__"
