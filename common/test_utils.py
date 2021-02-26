import json

from datetime import timedelta
from django.utils import timezone as dt

from poll.models import Poll, PollQuestion


def get_sngl_choice_answer():
    return json.dumps({'choiceType':PollQuestion.SNGL, 'choices':['Big D', 'Who knows?']})

def get_mltpl_choice_answer():
    return json.dumps({'choiceType':PollQuestion.MLTPL, 'choices':['Big D', 'Who knows?']})

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

def create_poll_question(poll, title='Have you ever had?', question_count=1 ):
    answ_choices = []
    for i in range(question_count):
        answ_choices.append(get_sngl_choice_answer())

    PollQuestion.objects.create(
                    poll=poll,
                    title=title,
                    answer_choices=answ_choices
        )

def create_poll_template():
    poll = create_poll()
    create_poll_question(poll, title='Question title 1', question_count=3)
    create_poll_question(poll, title='Question title 2', question_count=1)
    return poll
