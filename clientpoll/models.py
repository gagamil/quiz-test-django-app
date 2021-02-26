from django.db import models

from poll.models import Poll
from common.models import User


DEF_CHAR_FIELD_LENGTH = 200


class ClientPoll(models.Model):
    '''
    This is the active poll created when we expect to get the answers from the Client user.
    questions - Materialized View pattern with following shape:
    [ {pollTemplateQuestionId:121, title:'Hello world', choices:{choiceType:'SNGL'. choices:['What is the difference between props and state?',]}} ]
    Questions are already ordered.
    '''
    poll_template = models.ForeignKey(Poll, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    title = models.CharField(max_length=DEF_CHAR_FIELD_LENGTH)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.TextField()
    questions = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ClientPollAnswer(models.Model):
    '''
    This is the whole result set for the poll. JSON is sent by the frontend app.
    Сould be used for further processing. Ex: evaluation based on points or correctness.
    '''
    client_poll = models.OneToOneField(ClientPoll, on_delete=models.PROTECT)

    answer = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
