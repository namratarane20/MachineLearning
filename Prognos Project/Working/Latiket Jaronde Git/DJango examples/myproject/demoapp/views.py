from django.shortcuts import render

# Create your views here.


def index(request):
    msg = 'this is msg from view.py'
    return render(request, "application.html")

