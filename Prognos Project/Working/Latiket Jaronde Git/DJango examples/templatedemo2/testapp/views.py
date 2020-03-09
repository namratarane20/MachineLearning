from django.shortcuts import render
import datetime

# Create your views here.


def greeting(request):
    msg = "Hey nigga, Good "
    dt = datetime.datetime.now()
    h = int(dt.strftime('%H'))
    if 6 <= h <= 12:
        msg += "MORNING"
    elif h <= 16:
        msg += 'AFTERNOON'
    elif h <= 21:
        msg += "EVENING"
    else:
        msg += "NIGHT"

    return render(request, 'testapp/index.html', context={'msg': msg, 'time': dt})
