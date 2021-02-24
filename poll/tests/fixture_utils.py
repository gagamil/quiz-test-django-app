from datetime import timedelta
from django.utils import timezone as dt

from poll.models import Poll, PollQuestion


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