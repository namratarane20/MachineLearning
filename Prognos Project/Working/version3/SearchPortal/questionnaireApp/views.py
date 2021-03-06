from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm, ProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction

# Global Variables

globalRelaventId=[]
globalKeyword=''
globalRequiredData=[]
globalPolicyResult=[]
globalMostRelevantResponses=[]
globalMostRelevantData=''

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
    # Fetch keyword to be search
    keyword = request.POST['keyword']

    # Declare Global Keywords within this function
    global globalKeyword
    global globalPolicyResult
    global globalRequiredData
    global globalMostRelevantResponses
    global globalMostRelevantData



    # Fetch user from SSO
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2

    globalKeyword = keyword
    globalMostRelevantData = user+' '+globalKeyword
    sortedResponses = []
    sortedResponses1 = []
    policiesSearchResult = []

    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    questionnaireSearchResult = elasticSearchObject.search(index="question_naire",
                                                           size=9999,
                                                           body={
                                                               "query": {
                                                                   "match": {
                                                                       "SecurityQuestions": globalKeyword
                                                                   }
                                                               }
                                                           })

    questionnaireRequiredData = []  # data to be display in table
    questionnaireRequiredId = []
    mostRelevantResponses = []

    for hit in questionnaireSearchResult['hits']['hits']:
        questionnaireRequiredData.append(hit['_source'])  # extracting required data
        questionnaireRequiredId.append(hit['_id'])
        mostRelevantResponses.append(hit['_source']['MostRelevantResponses'])
    globalMostRelevantResponses = mostRelevantResponses
    print (questionnaireRequiredData)


    #  ID is added to the Data to get proper data when any operation is perform on data
    for a in range(len(questionnaireRequiredData)):
        questionnaireRequiredData[a].update({'ID': questionnaireRequiredId[a]})

    # Data is Sorted for Most Favourite Responses
    for data in questionnaireRequiredData:
        if globalMostRelevantData in data['MostRelevantResponses']:
            sortedResponses = [data] + sortedResponses
        else:
            sortedResponses1 = sortedResponses1 + [data]
    for i in sortedResponses1:
        sortedResponses.append(i)

    # this global Data to be user in relevantResponses method
    globalRequiredData = sortedResponses

    # Elastic search on Policy Data
    policiesResultList = elasticSearchObject.search(index='policies',
                                                    size=9999,
                                                    body={
                                                        'query': {
                                                            'match': {
                                                                'Data': globalKeyword
                                                            }
                                                        }
                                                    })

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

    # this global policy Data to be user in relevantResponses method
    globalPolicyResult = policiesSearchResult

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult,
               'questionnaireId': questionnaireRequiredId, 'MostRelevantData':globalMostRelevantData}

    return render(request, 'questionnaireApp/home.html', context)

def relevantResponses(request):
    # Fetch list of records to be most favourite through checkboxes
    fevButton = request.POST.getlist('fevButton[]')
    print(fevButton)

    # Declare Global Keywords within this function
    global globalKeyword
    global globalPolicyResult
    global globalRequiredData
    global globalKeywordSearch
    global globalMostRelevantResponses
    global globalMostRelevantData
    print (globalMostRelevantData)

    # Fetch user from SSO
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2


    sortedResponses = []
    sortedResponses1 = []

    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    try:
        # This is a loop to perform operation on selected records to be most favourite
        for id in fevButton:
            # here we get data which is selected by checkboxes
            relaventData = globalRequiredData[int(id) - 1]
            # here we get id of that selected data
            relaventId = relaventData.get('ID')
            print(relaventId)
            # after work of Id is done of comparision so to get correct records, it is deleted
            # relaventData.pop('ID')
            # This are the conditions to get update proper keyword to elastic search
            # If no data in column
        if relaventData['MostRelevantResponses'] == '':
            print("come under condition with empty data")
            relaventData['MostRelevantResponses'] = []
            relaventData['MostRelevantResponses'].append(globalMostRelevantData)
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)

        elif relaventData['MostRelevantResponses'] == []:
            print("come under condition with empty list")
            relaventData['MostRelevantResponses'].append(globalMostRelevantData)
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)

        elif globalMostRelevantData in relaventData['MostRelevantResponses']:
            print("come when similar data so delete")
            relaventData['MostRelevantResponses'].remove(globalMostRelevantData)
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)

        elif globalMostRelevantData not in relaventData['MostRelevantResponses']:
            print("not having similar data so add")
            relaventData['MostRelevantResponses'].append(globalMostRelevantData)
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)

        else:
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                      body=relaventData)

    except:
        pass

    # Data is again Sorted for getting data after submiting most revelent
    for data in globalRequiredData:
        if globalMostRelevantData in data['MostRelevantResponses']:
            sortedResponses = [data] + sortedResponses
        else:
            sortedResponses1 = sortedResponses1 + [data]
    for i in sortedResponses1:
        sortedResponses.append(i)

    # this global Data to be user in relevantResponses method
    globalRequiredData = sortedResponses

    context={'questionnaireResult': globalRequiredData,'policiesResult': globalPolicyResult,'MostRelevantData':globalMostRelevantData}

    return render(request,'questionnaireApp/home.html',context)

def indexQuestionnaireFile(request):
    from elasticsearch import Elasticsearch
    import csv
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    elasticSearchObject.indices.create(index='question_naire', ignore=400)  # creating index, ignore if already exists

    for csvFile in request.FILES.getlist('csvfile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file, encoding=request.encoding)  # to get text file
        reader = csv.DictReader(file)  # reading csv

        indexCounter = 1
        for row in reader:
            elasticSearchObject.index(index='question_naire', doc_type='document', id=str(csvFile) + str(indexCounter),
                                      body=row)  # indexing file
            indexCounter += 1

        try:
            while True:
                elasticSearchObject.delete(index='question_naire', doc_type='document',
                                           id=str(csvFile) + str(indexCounter))
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

