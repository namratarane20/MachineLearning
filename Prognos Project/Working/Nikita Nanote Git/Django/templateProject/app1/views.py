from django.shortcuts import render
import datetime
def temp_view(request):
    dt=datetime.datetime.now()
    mk=100
    rlno=132
    nm='nikita'
    my_dict={'date' : dt,'marks':mk,'roll_no':rlno,'name':nm}
    return render(request,'app1/result.html',context=my_dict)
