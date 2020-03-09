from django.http import HttpResponse
from django.shortcuts import render
# from questionnaireApp.models import EmployeeDetails
# Create your views here.
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
# from questionnaireApp.models import EmployeeDetails
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from .forms import UserForm,ProfileForm


# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    return render(request, 'questionnaireApp/home.html')


@login_required
@transaction.atomic

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# End of sign in functinality==========================================================================

# searching keyword in elasticsearch index
def searchKeyword(request):
    # This is a list which get the values of checkboxes
    keyword = request.POST['keyword']
    check_list = request.POST.getlist('check[]')
    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")





    #
    # if check_list == ['1']:
    #     question = True
    #
    #     questionnaireSearchResult = elasticSearchObject.search(index='questionnaire',
    #                                               size=9999,
    #                                               body={
    #                                                   "query": {
    #                                                       "match": {
    #                                                           "SecurityQuestions": keyword
    #                                                       }
    #                                                   }
    #                                               })
    #
    #     questionnaireRequiredData = []  # data to be display in table
    #     questionnnaireVendorNameSet = set({})
    #
    #     for hit in questionnaireSearchResult['hits']['hits']:
    #         questionnaireRequiredData.append(hit['_source'])  # extracting required data
    #         questionnnaireVendorNameSet.add(hit['_source']['VendorName'])
    #
    #     return render(request, 'questionnaireApp/home.html', {'questionnaireResult': questionnaireRequiredData, 'questionnaireVendorNameSet': questionnnaireVendorNameSet,'question':question})

    # if check_list == ['2']:
    #     policy = True
    #     policiesResultList = elasticSearchObject.search(index='policies',
    #                                                     size=9999,
    #                                                     body={
    #                                                         'query': {
    #                                                             'match': {
    #                                                                 'Data': keyword
    #                                                             }
    #                                                         }
    #                                                     })
    #     # print("result : ", resultList['hits']['hits'][0]['_source']['PolicyName'])
    #     policiesSearchResult = []
    #
    #     # extract a paragraph from which contains required keyword
    #     for i, hit in enumerate(policiesResultList['hits']['hits']):
    #         policiesSearchResult.append(hit['_source'])
    #         data = hit['_source']['Data']
    #         nextLineCharIndex = len(data) - (data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
    #         nextLineCharNextIndex = data.find("\n", nextLineCharIndex)
    #
    #         while True:
    #             if data[nextLineCharIndex:nextLineCharNextIndex].isupper():
    #                 data = data[nextLineCharNextIndex:]
    #                 nextLineCharIndex = len(data) - (
    #                     data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
    #                 nextLineCharNextIndex = data.find("\n", nextLineCharIndex)
    #             else:
    #                 break
    #
    #         policiesSearchResult[i]['Data'] = data[nextLineCharIndex:nextLineCharNextIndex]
    #
    #     return render(request, "questionnaireApp/home.html", {'policiesResult': policiesSearchResult, 'policy': policy})
    #
    question = True
    policy = True
    both = True
    if check_list == ['1', '2']:
        both = True
        questionnaireSearchResult = elasticSearchObject.search(index="questionnaire",
                                                  size=9999,
                                                  body={
                                                      "query": {
                                                          "match": {
                                                              "SecurityQuestions": keyword
                                                          }
                                                      }
                                                  })

        questionnaireRequiredData = []  # data to be display in table
        questionnnaireVendorNameSet = set({})

        for hit in questionnaireSearchResult['hits']['hits']:
            questionnaireRequiredData.append(hit['_source'])  # extracting required data
            questionnnaireVendorNameSet.add(hit['_source']['VendorName'])

        policiesResultList = elasticSearchObject.search(index='policies',
                                       size=9999,
                                       body={
                                           'query': {
                                               'match': {
                                                   'Data': keyword
                                               }
                                           }
                                       })
        # print("result : ", resultList['hits']['hits'][0]['_source']['PolicyName'])
        policiesSearchResult = []

        # extract a paragraph from which contains required keyword
        for i, hit in enumerate(policiesResultList['hits']['hits']):
            policiesSearchResult.append(hit['_source'])
            data = hit['_source']['Data']
            nextLineCharIndex = len(data) - (data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
            nextLineCharNextIndex = data.find("\n", nextLineCharIndex)

            while True:
                if data[nextLineCharIndex:nextLineCharNextIndex].isupper():
                    data = data[nextLineCharNextIndex:]
                    nextLineCharIndex = len(data) - (
                        data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
                    nextLineCharNextIndex = data.find("\n", nextLineCharIndex)
                else:
                    break

            policiesSearchResult[i]['Data'] = data[nextLineCharIndex:nextLineCharNextIndex]

        context = {'questionnaireResult': questionnaireRequiredData, 'questionnaireVendorNameSet': questionnnaireVendorNameSet, 'policiesResult': policiesSearchResult, 'both': both}
        return render(request, 'questionnaireApp/home.html', context)
    if check_list==[]:
        return render(request, 'questionnaireApp/home.html')


def indexQuestionnaireFile(request):
    from elasticsearch import Elasticsearch
    import csv
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    elasticSearchObject.indices.create(index='questionnaire', ignore=400)  # creating index, ignore if already exists

    for csvFile in request.FILES.getlist('csvfile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file, encoding=request.encoding)  # to get text file
        reader = csv.DictReader(file)  # reading csv

        indexCounter = 1
        for row in reader:
            elasticSearchObject.index(index='questionnaire', doc_type='document', id=str(csvFile) + str(indexCounter),
                                      body=row)  # indexing file
            indexCounter += 1

        try:
            while True:
                elasticSearchObject.delete(index='questionnaire', doc_type='document', id=str(csvFile) + str(indexCounter))
                indexCounter += 1
        except:
            pass

    return render(request, 'questionnaireApp/uploadFile.html')


def indexPoliciesFile(request):
    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
    elasticSearchObject.indices.create(index="policies", ignore=400)
    for docFile in request.FILES.getlist('policyFile'):
        fileName = str(docFile)[:str(docFile).rfind('.')]
        from docx import Document
        document = Document(docFile)
        textList = []
        for paragraph in document.paragraphs:
            textList.append(paragraph.text)
        textData = '\n'.join(textList)
        data = {'PolicyName': fileName, 'Data': textData, 'Link': request.POST['link']}
        elasticSearchObject.index(index='policies', id=fileName, body=data)

    return render(request, 'questionnaireApp/uploadFile.html')


def adminLogin(request):
    return render(request, "questionnaireApp/adminLogin.html")


def adminMailVerification(request):
    emailId = 'admin@prognoshealth.com'
    password = 'admin@321'
    if emailId == request.POST['emailId']:
        if password == request.POST['password']:
            return render(request, "questionnaireApp/uploadFile.html")
        else:
            message = 'please enter valid password'
            return render(request, "questionnaireApp/adminLogin.html", {'message': message})
    else:
        message = 'please enter valid Email ID'
        return render(request, "questionnaireApp/adminLogin.html", {'message': message})


def toHomePage(request):
    return render(request, 'questionnaireApp/home.html')

#
# def userLogin(request):
#     return render(request, 'questionnaireApp/userLogin.html')

#
# def mailVerification(request):
#     emailData = request.POST['emailId']
#     employeeList = EmployeeDetails.objects.all()
#     for employee in employeeList:
#         if employee.employeeEmail == emailData:
#             return render(request, 'questionnaireApp/home.html')
#
#         else:
#             validate = True
#             return render(request, 'questionnaireApp/userLogin.html', {'validate': validate})




