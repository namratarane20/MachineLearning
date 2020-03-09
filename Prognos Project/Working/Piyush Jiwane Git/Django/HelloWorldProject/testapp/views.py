from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world_view(request):
    return HttpResponse('<h1> Hello piyush...from Django application </h1>')