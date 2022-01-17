from rest_framework import serializers
from .models import (
    Explanation,
)


class ExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ("verse", "comment", "author")
