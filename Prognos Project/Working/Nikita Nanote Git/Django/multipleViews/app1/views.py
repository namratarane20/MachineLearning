from django.http import HttpResponse
import datetime as dt
date1=dt.datetime.now()
def date(request):
    date='The current date and time is :',date1
    d1='Year is : ',date1.year
    return HttpResponse(date)
def home(request):
    x='This is home page'
    return HttpResponse(x)
def contact(request):
    y='This is my contact'
    return HttpResponse(y)