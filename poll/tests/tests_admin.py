from datetime import timedelta
import json
import io

#from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as dt
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from common.test_utils import get_sngl_choice_answer, get_mltpl_choice_answer
from common.models import User
from poll.models import Poll, PollQuestion
from poll.serializers_admin import PollListSerializer


def get_start_finish_dates():
    start_date = dt.localdate() + timedelta(days=1)
    finish_date = dt.localdate() + timedelta(days=3)
    return start_date, finish_date

def create_poll():
    start_date, finish_date = get_start_finish_dates()
    return Poll.objects.create(
                    title='Supreme poll',
                    start_date = start_date,
                    finish_date=finish_date,
                    description='How much?'
        )

def create_poll_question(poll, title='Have you ever had?'):
    return PollQuestion.objects.create(
                    poll=poll,
                    title=title
        )

def create_admin_user():
    return User.objects.create(username='admin001', role=User.ROLE_ADMINISTRATOR)



class BasicAdminPollTests(APITestCase):
    def setUp(self):
        user = create_admin_user()
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_poll(self):
        start_date, finish_date = get_start_finish_dates()
        # start_date_str = json.dumps(start_date, cls=DjangoJSONEncoder)
        # finish_date_str = json.dumps(finish_date, cls=DjangoJSONEncoder)
        url = reverse('create-poll')
        data = {
                'title': 'My new cool poll',
                'start_date':start_date,
                'finish_date':finish_date,
                'description':'Lorem ipsum...'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 1)
    
    def test_update_poll(self):
        poll = create_poll()
        self.assertEqual(Poll.objects.count(), 1)

        new_title = 'Oh la la'
        new_finish_date = dt.localdate() + timedelta(days=3)
        new_description = 'There is something wrong with the world today...'
        url = reverse('update-poll', kwargs={'pk':poll.pk})
        data = {
                'title': 'Oh la la',
                'finish_date':new_finish_date,
                'description':new_description
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(Poll.objects.filter(title=new_title, description=new_description).count(), 1)

    def test_destroy_poll(self):
        poll = create_poll()
        self.assertEqual(Poll.objects.count(), 1)

        url = reverse('destroy-poll', kwargs={'pk':poll.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Poll.objects.count(), 0)


class BasicAdminPollQuestionTests(APITestCase):
    def setUp(self):
        user= create_admin_user()
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.poll = create_poll()

    def test_poll_question_ordinals(self):
        create_poll_question(self.poll, 'Question A')
        create_poll_question(self.poll, 'Question B')
        create_poll_question(self.poll, 'Question C')

        self.assertEqual(list(self.poll.get_pollquestion_order()), [1,2,3])
        self.poll.set_pollquestion_order([3, 1, 2])
        self.assertEqual(list(self.poll.get_pollquestion_order()), [3,1,2])
        create_poll_question(self.poll, 'Question D')
        self.assertEqual(list(self.poll.get_pollquestion_order()), [3,1,2,4])
    
    def test_poll_question_ordinals_endpoint(self):
        create_poll_question(self.poll, 'Question A')
        create_poll_question(self.poll, 'Question B')
        create_poll_question(self.poll, 'Question C')

        # 1st GET run - just to be clear that default ordering is: [1,2,3]
        url = reverse('fetch-poll-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Poll.client_objects.count(), 1)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data[0]['ordered_question_ids'], [1,2,3])

        # Now update ordering via API endpoint to [3,1,2]
        url = reverse('update-poll-ordering', kwargs={'pk':self.poll.pk})
        data = {'ordered_question_ids': [3,1,2]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 2nd GET run - just to be clear that default ordering is: [3,1,2]
        url = reverse('fetch-poll-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Poll.client_objects.count(), 1)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data[0]['ordered_question_ids'], [3,1,2])


    def test_create_poll_question_string(self):
        url = reverse('create-poll-question', kwargs={'poll_pk':self.poll.pk})
        data = {
                'poll': self.poll.pk,
                'title':'Who is your daddy?',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PollQuestion.objects.get().choice_type, None)
    
    def test_create_poll_question_sngl(self):
        url = reverse('create-poll-question', kwargs={'poll_pk':self.poll.pk})
        data = {
                'poll': self.poll.pk,
                'title':'Who is your daddy?',
                'answer_choices':get_sngl_choice_answer()
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PollQuestion.objects.count(), 1)
        self.assertEqual(PollQuestion.objects.get().choice_type, PollQuestion.SNGL)

    def test_create_poll_question_mltpl(self):
        url = reverse('create-poll-question', kwargs={'poll_pk':self.poll.pk})
        data = {
                'poll': self.poll.pk,
                'title':'Who is your daddy?',
                'answer_choices':get_mltpl_choice_answer()
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PollQuestion.objects.count(), 1)
        self.assertEqual(PollQuestion.objects.get().choice_type, PollQuestion.MLTPL)

    def test_update_poll_question(self):
        '''
        Create poll question
        1) Change only title
        2) Change title and type (leave poll id same)
        '''
        poll_question = create_poll_question(self.poll)
        self.assertEqual(PollQuestion.objects.count(), 1)

        url = reverse('update-poll-question', kwargs={'poll_pk':self.poll.pk, 'pk':poll_question.pk})
        data = {
                'poll': self.poll.pk,
                'title':'Who is your daddy?',
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PollQuestion.objects.get().choice_type, None)

        self.assertEqual(PollQuestion.objects.count(), 1)

        data = {
                'poll': self.poll.pk,
                'title':'Who is your daddy?',
                'answer_choices':json.dumps({'choiceType':PollQuestion.MLTPL, 'choices':['Big D', 'Who knows?']})
                }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PollQuestion.objects.count(), 1)
        self.assertEqual(PollQuestion.objects.get().choice_type, PollQuestion.MLTPL)

    def test_destroy_poll_question(self):
        poll_question = create_poll_question(self.poll)
        self.assertEqual(PollQuestion.objects.count(), 1)

        url = reverse('destroy-poll-question', kwargs={'poll_pk':self.poll.pk, 'pk':poll_question.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PollQuestion.objects.count(), 0)