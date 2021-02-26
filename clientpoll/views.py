
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from poll.models import Poll
from .models import ClientPoll
from .serializers import ClientPollCreateSerializer, ClientPollAnswerCreateSerializer


class ClientPollCreateView(generics.CreateAPIView):
    serializer_class = ClientPollCreateSerializer

    def perform_create(self, serializer):
        poll = serializer.validated_data['poll_template']
        serializer.save(
            user=self.request.user, 
            questions=poll.questions_json,
            title=poll.title,
            start_date=poll.start_date,
            finish_date=poll.finish_date,
            description=poll.description
            )


class ClientPollAnswerCreateView(generics.CreateAPIView):
    serializer_class = ClientPollAnswerCreateSerializer