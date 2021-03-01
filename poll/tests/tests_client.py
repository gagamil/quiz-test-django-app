import io
import time_machine
from django.urls import reverse
from django.utils import timezone as dt
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from common.models import User
from poll.models import Poll, PollQuestion
from poll.serializers_client import PollListSerializer
from .fixture_utils import create_poll


def create_client_user():
    return User.objects.create(username='admin001', role=User.ROLE_SIMPLE)


class BasicClientPollTests(APITestCase):

    def test_fetch_poll_list_success(self):
        url = reverse('client-fetch-poll-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Poll.client_objects.count(), 0)

        create_poll()

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Poll.client_objects.count(), 1)

    def test_fetch_poll_list_fail_due_to_date_miss(self):
        with time_machine.travel(0, tick=False) as traveller:
            create_poll()

            url = reverse('client-fetch-poll-list')
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Poll.client_objects.count(), 1)

            stream = io.BytesIO(response.content)
            data = JSONParser().parse(stream)
            serializer = PollListSerializer(data=data, many=True)
            serializer.is_valid()
            self.assertEqual(len(serializer.validated_data), 1)

            traveller.shift(dt.timedelta(days=10))

            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Poll.client_objects.count(), 0)

            stream = io.BytesIO(response.content)
            data = JSONParser().parse(stream)
            serializer = PollListSerializer(data=data, many=True)
            serializer.is_valid()
            self.assertEqual(len(serializer.validated_data), 0)