from rest_framework import serializers

from .models import Forest


class ForestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = "__all__"
