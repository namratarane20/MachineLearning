from django.http import HttpResponse
def greetings(request):
    msg='<h1>Welcome Friends...Good Morning to all </h1>'
    return HttpResponse(msg)

