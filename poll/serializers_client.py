from rest_framework import serializers

from .models import Poll, PollQuestion


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'finish_date', 'description']