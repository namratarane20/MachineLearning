from django.shortcuts import render
import datetime
from django.http import HttpResponse
# Create your views here.


def date_time(request):
    dt = datetime.datetime.now()
    s = "<h1>current time is : " + str(dt) + "<h1>"
    return HttpResponse(s)
