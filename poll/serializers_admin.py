from rest_framework import serializers

from .models import Poll, PollQuestion


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'start_date', 'finish_date', 'description', 'ordered_question_ids']


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['title', 'start_date', 'finish_date', 'description']


class PollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['title', 'finish_date', 'description']


class PollUpdateOrderingSerializer(serializers.Serializer):
    ordered_question_ids = serializers.ListField(child=serializers.IntegerField())
    class Meta:
        model = Poll
        fields = []
        read_only_fields = ['ordered_question_ids']


class PollQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ['poll', 'title', 'answer_choices']


class PollQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ['poll', 'title', 'answer_choices']