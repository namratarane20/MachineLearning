from django.shortcuts import render
import datetime
def wish(request):
    date=datetime.datetime.now()
    h1=int(date.strftime("%H"))
    msg='hey Guyz !!!  Good '
    if h1<12:
        msg=msg+'Morning'
    elif h1<16:
        msg=msg+'Afternoon'
    elif h1<20:
        msg=msg+'Evening'
    else:
        msg=msg+'Night'
    my_dict={'date':date,'msg':msg}
    return render(request,"app1/result.html",my_dict)