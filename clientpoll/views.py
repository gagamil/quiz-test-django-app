
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.models import User
from poll.models import Poll
from .models import ClientPoll, ClientPollAnswer
from .serializers import ClientPollCreateSerializer, ClientPollAnswerCreateSerializer


def get_user(request, username):
        if request.user.is_authenticated:
            return request.user
        u, _ = User.objects.get_or_create(username=username, role=User.ROLE_SIMPLE)
        return u

    
class ClientPollCreateView(generics.CreateAPIView):
    '''
    Not using std permissions because have to let non auth requests here.
    Could use custom permission and bitwise or - but this was a bit more straightforward for the purpose
    '''
    serializer_class = ClientPollCreateSerializer

    def create(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            request.data['user'] = self.request.user.username
        else:
            user, _ = User.objects.get_or_create(username=request.data['user'], role=User.ROLE_SIMPLE)
            request.data['user'] = user.username
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        poll = serializer.validated_data['poll_template']
        user = get_user(self.request, serializer.validated_data['user'])
        serializer.save(
            user=user, 
            questions=poll.questions_json,
            title=poll.title,
            start_date=poll.start_date,
            finish_date=poll.finish_date,
            description=poll.description
            )


class ClientPollAnswerCreateView(generics.CreateAPIView):
    '''
    Not using std permissions because have to let non auth requests here.
    Could use custom permission and bitwise or - but this was a bit more straightforward for the purpose
    '''
    serializer_class = ClientPollAnswerCreateSerializer

    def create(self, request, *args, **kwargs):
        user = None
        
        if self.request.user.is_authenticated:
            request.data['user'] = self.request.user.username
        else:
            user_id = request.data['user']
            user, _ = User.objects.get_or_create(username=user_id, role=User.ROLE_SIMPLE)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        poll = serializer.validated_data['client_poll']
        answer = serializer.validated_data['answer']
        user = get_user(self.request, serializer.validated_data['user'])
        ClientPollAnswer.objects.create(client_poll=poll, answer=answer)