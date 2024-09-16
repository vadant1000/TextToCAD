from rest_framework import serializers
from visual_api.models import Visual


class VisualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visual
        fields = "__all__"

