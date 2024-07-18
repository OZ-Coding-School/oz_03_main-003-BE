from rest_framework import serializers
from .models import Forest
from trees.models import TreeMap

class TreeMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeMap
        fields = '__all__'

class ForestSerializer(serializers.ModelSerializer):
    trees = TreeMapSerializer(many=True, read_only=True)

    class Meta:
        model = Forest
        fields = '__all__'
