from rest_framework import serializers

from .models import Poll, PollQuestion

class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['title', 'start_date', 'finish_date', 'description']

class PollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['title', 'finish_date', 'description']

class PollQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ['poll', 'title', 'answer_choices']