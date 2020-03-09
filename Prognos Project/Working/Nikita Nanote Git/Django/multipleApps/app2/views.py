from django.http import HttpResponse
import datetime as dt
def timeLine(request):
    date=dt.datetime.now()
    s='Current date is'+str(date.date())+' <br> time is :'+str(date.time())
    return HttpResponse(s)