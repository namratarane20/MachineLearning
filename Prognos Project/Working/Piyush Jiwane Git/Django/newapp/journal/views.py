from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'days':['Piyush','Gaurav'],
        'listOfDict':[{'Piyush':'Jiwane'},{'gaurav':'jiwane'}]
    }
    return render(request,'index.html',context)