import csv
import datetime
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from elasticsearch import  Elasticsearch
from djangodemo.models import EmpolyeeDetails
from  .models import EmpolyeeDetails
from djangodemo.forms import EmpolyeeDetailsForm
import sqlite3
# Create your views here.
elasticSearchObj = Elasticsearch(
    "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")


# this is function for to jump to login page
def renderToLogin(request):
    return render(request,'djangodemo/loginPage.html')


# this function is to check the username from data base Employee is available then jump to serach or home page
def userLogin(request):
    emailData = request.POST['emailId']
    emp = EmpolyeeDetails.objects.all()
    for e in emp:
        if e.eemail == emailData:
            # success =False
            print(e.eemail)
            return render(request,'djangodemo/homepage.html')
        else:
            validate = True
            return render(request,'djangodemo/loginPage.html',{'validate':validate})



# this is function to get the data from table
def displayUser(request):
    emp = EmpolyeeDetails.objects.all()
    for e in emp:
        print(e.eemail)
    return render(request,'djangodemo/admin.html',{'emp':emp})

def deleteUser(request):

     #
     # empdata = EmpolyeeDetails.objects.get(e.eemail)
     # empdata.delete()

     # empdata = EmpolyeeDetails.objets.create_user()

     ename = EmpolyeeDetails.objects.get(request.POST['chk'])
     # eemail = EmpolyeeDetails.objects.get(request.POST['chk'])
     ename.delete()
     # eemail.delete()
     msg = 'user deleted -------- successfully'

     return render(request, 'djangodemo/admin.html', {'msg': msg})

        # return render(request, 'ur template where you want to redirect')
     return render(request, 'djangodemo/admin.html')


# rom
# django.shortcuts
# import render
#  from .models import Post


def addUser(request):
       ename= request.POST.get("ename")
       eemail=request.POST.get("eemail")
       empData=EmpolyeeDetails(ename=ename,eemail=eemail)
       empData.save()
       msg = 'user added successfully'
       return render(request, 'djangodemo/admin.html',{'msg':msg})


#this function to search keyword from elastic serach data
def serachKeyword(request):
    keyword =request.POST['keyword']
    searchResult = elasticSearchObj.search(index='questionnaire_demo',
                                           size = 9999,
                                           body={
                                               "query":{
                                                   "match":{
                                                       "SecurityQuestions":keyword
                                                   }
                                               }
                                           }
                                           )
    print(searchResult)

    requiredData=[]
    venderNameset = set({})

    for hit in searchResult['hits']['hits']:
         requiredData.append(hit['_source']) # exatract required data
         venderNameset.add(hit['_source']['VendorName'])

         print(type(venderNameset))
         print(venderNameset)


    return render(request,'djangodemo/homepage.html',{'result':requiredData,'nameSet':venderNameset})


# this function is to perfrom upload option from frontend
def uploadcsv(request):
    return  render(request,'djangodemo/uploadFile.html')

def toHomePage(request):
    return render(request, 'djangodemo/homepage.html')


def indexFile(request):

    # elasticSearchObj.indices.create(index='elasticsearc', ignore=400)  # creating index, ignore if already exists
    elasticSearchObj.indices.create(index='questionnaire_demo', ignore=400)
    for csvFile in request.FILES.getlist('csvfile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file, encoding=request.encoding)  # to get text file
        reader = csv.DictReader(file)  # reading csv

        indexCounter = 1
        for row in reader:
            elasticSearchObj.index(index='questionnaire_demo', doc_type='document', id=str(csvFile) + str(indexCounter),
                                      body=row)  # indexing file
            indexCounter += 1

        try:
            while True:
                elasticSearchObj.delete(index='questionnaire_demo', doc_type='document', id=str(csvFile) + str(indexCounter))
                indexCounter += 1
        except:
            pass

    return render(request, 'djangodemo/uploadFile.html')

def toSerachPage(request):
    return render(request,'djangodemo/homepage.html')















# def demoFun(request):
#     return render(request, 'djangodemo/result.html')
#     # # return  return  render(request,'demoapp/result.html')
#     #  return  render(request,'djangodemo/result.html')
# def wish(request):
#     date=datetime.datetime.now()
#    # h = int(date.strftime('%H'))
#    #  h=15
#     h=3
#     msg=' '
#     # if h<12:
#     #     msg=msg+'Morning!!!!'
#     # elif h<16:
#     #     msg=msg+'Afternoon'
#     # elif h<21:
#     #     msg=msg+'Evening'
#     # else:
#     #     msg=msg+'Night'
#     # response = render(request,'djangodemo/result.html',{'msgKey':msg,'dateKey':date})
#     # return response
#
#     if h<12:
#        msg=msg+'Morning'
#        return render(request,'djangodemo/morning.html',{'msgKey':msg,'dateKey':date})
#     elif h<16:
#        msg = msg + 'Afternoon'
#        return render(request,'djangodemo/afternoon.html',{'msgKey':msg,'dateKey':date})
#     elif h<21:
#        msg=msg+'Evening'
#        return render(request,'djangodemo/even.html',{'msgKey':msg,'dateKey':date})
#     else:
#        msg = msg + 'Night'
#        return render(request, 'djangodemo/night.html', {'msgKey': msg, 'dateKey': date})
