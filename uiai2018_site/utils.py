import pytz
import datetime
import jdatetime
from django.utils import timezone


def get_jdatetime(dt):
    d = jdatetime.date.fromgregorian(date=dt)
    t = timezone.localtime(dt, pytz.timezone('Iran'))
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
