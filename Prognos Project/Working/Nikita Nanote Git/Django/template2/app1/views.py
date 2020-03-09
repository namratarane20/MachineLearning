from django.shortcuts import render
import datetime
def wish(request):
    date=datetime.datetime.now()
    h1=int(date.strftime('%H'))
    msg='Hey guyz!! Good '
    if h1<12 :
        msg=msg+'Morning'
    elif h1<16 :
        msg=msg+'Afternoon'
    elif h1<21 :
        msg=msg+'Evening'
    else :
        msg=msg+'Night'
    return render(request,'app1/result.html',{'m':msg,'date':date})
