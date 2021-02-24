from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.views import AdminOnly
from .models import Poll, PollQuestion
from .serializers_admin import PollCreateSerializer, PollUpdateSerializer, PollQuestionCreateSerializer, \
    PollQuestionUpdateSerializer


class PollCreateView(generics.CreateAPIView):
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated&AdminOnly]


class PollUpdateView(generics.UpdateAPIView):
    serializer_class = PollUpdateSerializer
    permission_classes = [IsAuthenticated&AdminOnly]

    def get_queryset(self):
        return Poll.objects.all()


class PollDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated&AdminOnly]
    def get_queryset(self):
        return Poll.objects.all()


class PollQuestionCreateView(generics.CreateAPIView):
    serializer_class = PollQuestionCreateSerializer
    permission_classes = [IsAuthenticated&AdminOnly]


class PollQuestionUpdateView(generics.UpdateAPIView):
    serializer_class = PollQuestionUpdateSerializer
    permission_classes = [IsAuthenticated&AdminOnly]

    def get_queryset(self):
        return PollQuestion.objects.all()


class PollQuestionDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated&AdminOnly]
    def get_queryset(self):
        return PollQuestion.objects.all()