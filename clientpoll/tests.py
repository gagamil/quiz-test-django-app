from django.urls import reverse
from django.utils import timezone as dt
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.parsers import JSONParser

from common.models import User
from common.test_utils import create_poll_template
from poll.models import Poll, PollQuestion
from .models import ClientPoll, ClientPollAnswer


def create_client_user():
    return User.objects.create(username='admin001', role=User.ROLE_SIMPLE)

class BasicClientPollTests(APITestCase):
    fixtures = ['poll.json']
    def setUp(self):
        self.user = create_client_user()
        self.client.force_authenticate(user=self.user)
        self.poll = Poll.objects.get()

    def test_create_poll(self):
        self.assertEqual(Poll.objects.count(), 1)

        url = reverse('create-client-poll')
        data = {
                'poll_template': self.poll.pk,
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClientPoll.objects.count(), 1)
        # print(ClientPoll.objects.get(pk=1).questions)

    def test_post_poll_result_success(self):
        client_poll = ClientPoll.objects.create(
            poll_template=self.poll,
            user=self.user,
            title=self.poll.title,
            start_date=self.poll.start_date,
            finish_date=self.poll.finish_date,
            description=self.poll.description,
            questions=self.poll.questions_json
            )
        poll_answer_data = [
            {'pollTemplateQuestionId':1, 'answer':['Up to 7 years']},
            {'pollTemplateQuestionId':2, 'answer':['React', 'Django', 'GCP']},
            {'pollTemplateQuestionId':3, 'answer':['Knows how to ask questions. Knows his weak and strong points. Has solid experience in his domain.']}
            ]
        url = reverse('create-client-poll-result')
        data = {
                'client_poll': self.poll.pk,
                'answer': poll_answer_data
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClientPollAnswer.objects.count(), 1)
        print(response.content)
    
    def test_post_poll_result_fail(self):
        self.assertEqual(ClientPollAnswer.objects.count(), 0)
        
        client_poll = ClientPoll.objects.create(
            poll_template=self.poll,
            user=self.user,
            title=self.poll.title,
            start_date=self.poll.start_date,
            finish_date=self.poll.finish_date,
            description=self.poll.description,
            questions=self.poll.questions_json
            )
        poll_answer_data = [
            {'pollTemplateQuestionId':99999999, 'answer':['Up to 7 years']},
            {'pollTemplateQuestionId':2, 'answer':['React', 'Django', 'GCP']},
            {'pollTemplateQuestionId':3, 'answer':['Knows how to ask questions. Knows his weak and strong points. Has solid experience in his domain.']}
            ]
        url = reverse('create-client-poll-result')
        data = {
                'client_poll': self.poll.pk,
                'answer': poll_answer_data
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ClientPollAnswer.objects.count(), 0)
        print(response.content)


        