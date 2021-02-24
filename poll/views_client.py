
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Poll, PollQuestion
from .serializers_client import PollListSerializer


class PollListView(generics.ListAPIView):
    serializer_class = PollListSerializer

    def get_queryset(self):
        return Poll.client_objects.all()