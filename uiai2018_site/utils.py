import pytz
import datetime
import jdatetime
from django.utils import timezone


def get_jdatetime(dt):
    d = jdatetime.date.fromgregorian(date=dt)
    t = timezone.localtime(dt, pytz.timezone('Iran'))
    strdate = str(d.year) + '/' + str(d.month) + '/' + str(d.day)
    strtime = t.strftime('%H:%M')
    print(strdate, strtime)
    return strdate + ' - ' + strtime
