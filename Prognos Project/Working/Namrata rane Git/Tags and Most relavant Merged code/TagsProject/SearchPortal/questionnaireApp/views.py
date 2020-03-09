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
from .models import TagWithInfo

# Global Variables
globalRelaventId=[]
globalKeyword=''
globalRequiredData=[]
globalPolicyResult=[]
globalMostRelevantResponses=[]
globalKeywordSearch=[]


# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    return addToTags(request)

@login_required
@transaction.atomic
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
# End of sign in functinality==========================================================================

# searching keyword in elasticsearch index
globalTags = []
def searchKeyword(request):
    # Fetch keyword to be search
    keyword = request.POST['keyword']

    # Declare Global Keywords within this function
    global globalKeyword
    global globalPolicyResult
    global globalRequiredData
    global globalMostRelevantResponses
    global globalKeywordSearch

    # Fetch user from SSO
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2

    globalKeyword = keyword
    sortedResponses = []
    sortedResponses1 = []
    policiesSearchResult = []

    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    questionnaireSearchResult = elasticSearchObject.search(index="security_questionnaire",
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
    keywordSearched = []

    for hit in questionnaireSearchResult['hits']['hits']:
        questionnaireRequiredData.append(hit['_source'])  # extracting required data
        questionnaireRequiredId.append(hit['_id'])
        mostRelevantResponses.append(hit['_source']['MostRelevantResponses'])
        keywordSearched.append(hit['_source']['KeywordSearched'])
    globalMostRelevantResponses = mostRelevantResponses
    globalKeywordSearch = keywordSearched


    #  ID is added to the Data to get proper data when any operation is perform on data
    for a in range(len(questionnaireRequiredData)):
        questionnaireRequiredData[a].update({'ID': questionnaireRequiredId[a]})

    # Data is Sorted for Most Favourite Responses
    for data in questionnaireRequiredData:
        if user in data['MostRelevantResponses'] and globalKeyword in data['KeywordSearched']:
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

    tagNameList = []
    allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
    for tags in allTagNameColoumn:
        tagNameList.append(tags.tagName)
        tagNameList = list(dict.fromkeys(tagNameList))

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult,
               'questionnaireId': questionnaireRequiredId, 'keyword': globalKeyword, 'user1': user,'tagNameList':tagNameList}

    return render(request, 'questionnaireApp/home.html', context)


def toHomePage(request):
    return addToTags(request)

def addToTags(request):

    global globalTags
    print('inside addtotag function.........................................................')

    # tagNameAndUsernameDict = {}
    dateUserTagDict = {}
    tempDict ={}

    checkBoxList = request.POST.getlist('tagCheckbox[]')
    # addedtags = globalTags[int(checkBoxList) - 1]
    # print(globalTags)
    global userName
    userName = request.user.get_full_name()
    print(userName)
    tagsList = [] # to add all dict means all selected rows in list to make list of dict.
    try:
        for eachTagRow in checkBoxList:
            addedTags = globalTags[int(eachTagRow) - 1]
            # print("added tags : ", addedTags)
            # print("type : ", type(addedTags))
            tagsList.append(addedTags)
            print('data list ========',tagsList)
        for data in tagsList:
                col1 = data['VendorName']
                col2 = data['SectionName']
                col3 = data['ControlName']
                col4 = data['SecurityQuestions']
                col5 = data['ServiceSolutionResponse']
                col6 = data['ServiceSolutionComments']
                tagname = request.POST['tagname']
                tagDesc = request.POST['tagDescription']
                print('data=============================',tagDesc)
                if tagDesc == '':
                   print('data is empty--------------------------------')
                   tagDescQuerySet = TagWithInfo.objects.filter(tagName=tagname).values()

                   tagDescList = list(tagDescQuerySet)
                   for tagDescription in tagDescList:
                      tagDesc = tagDescription.get("tagDescription")
                      print('this is previous description', tagDesc)
                      print(type(tagDesc))
                else:
                      tagDesc=request.POST['tagDescription']

                userName = request.user.get_full_name()
                print('username saved with tagname',userName)
                # currentDate  = datetime.now()
                # tagCreatedTime = currentDate.strftime("%m/%d/%Y, %H:%M:%S")
                questionnaireObj =TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3,
                                              securityquestion=col4, response=col5, additionalcomment=col6,
                                              tagName=tagname,tagDescription= tagDesc,userName = userName)

                questionnaireObj.save()
        print('data saved succesfully ')


        # logic to pass tag name and user names as dict( keys and values)
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        # allData = list(allTagNameColoumn)  # list of dict
        for tagData in allTagNameColoumn:
            dateUserTagDict.update({tagData.tagName :{tagData.userName:tagData.dateTime}})
            print('my tags data are2222222222',dateUserTagDict)

        return render(request, 'questionnaireApp/demo.html', {'dateUserTagDict':dateUserTagDict})
    except Exception as e:
         print("exception occured : ", e)
        # # pass
         return render(request, 'questionnaireApp/demo.html',{'dateUserTagDict':dateUserTagDict})


def displayTagInformation(request, tagname):
    print("selected tag name : ", tagname)
    databaseTags = TagWithInfo.objects.filter(tagName = tagname).values()
    # print('new data',databaseTags)
    # print(type(databaseTags)) # // quesySet
    # databaseTags are filter data from database where tag name is available (tag name is getting from front end )
    addedTagdata= list(databaseTags)
    print(addedTagdata)
    print(type(addedTagdata)) # this is list of dict data
    tagDesc =[]
    for tagDescription in addedTagdata:

        # print(tagDescription)
        # print(type(tagDescription))
        # tagDesc.append(tagDescription.get("tagDescription"))
        tagDesc = tagDescription.get("tagDescription")

        print('this is previous description',tagDesc)
        print(type(tagDesc))



    return render(request, "questionnaireApp/TagTable.html", {'addedTagdata': addedTagdata, 'selectedTagName':tagname,'tagDesc':tagDesc})


def destroyTagInformation(request):
    print('inside destroy function=======================')
    print(request.POST['destroyedTagName'])
    destroyedTagName = request.POST['destroyedTagName']
    destroyTagsData = TagWithInfo.objects.filter(tagName = destroyedTagName).update(flag = 0)
    flag0data = TagWithInfo.objects.filter(tagName = destroyedTagName ).values()
    print('data of destroyed tag =======',flag0data)
    return addToTags(request)




def relevantResponses(request):
   # Fetch list of records to be most favourite through checkboxes
   fevButton = request.POST.getlist('fevButton[]')
   flag=request.POST['flag']
   flag1=int(flag)
   print(fevButton)
   print(flag)
   # Declare Global Keywords within this function
   global globalKeyword
   global globalPolicyResult
   global globalRequiredData
   global globalKeywordSearch
   global globalMostRelevantResponses


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

           print(type(relaventData['KeywordSearched']))
           # here we get id of that selected data
           relaventId=relaventData.get('ID')
           print("***")
           print(relaventId)
           # after work of Id is done of comparision so to get correct records, it is deleted
           # relaventData.pop('ID')

           # This are the conditions to get update proper keyword to elastic search
           # If no data in column
       if relaventData['KeywordSearched'] == [] :
           print("come under condition with empty data")
           print(flag1)
           if flag1 == 1 :
               print("flag 1")
               relaventData['KeywordSearched']=globalKeyword
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 == 0:
               print("flag 0")
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
           # If list of data contain only one element which is similar to the keyword search
       elif globalKeyword in relaventData['KeywordSearched'] :
           if flag1 == 1:
               print("flag 11")
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 == 0:
               print("flag 00")
               relaventData['KeywordSearched']=relaventData['KeywordSearched'].replace(globalKeyword,'')
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
           # # If list of data contains the keyword search
           # elif globalKeyword in relaventData['KeywordSearched'] :
           #     if flag1 == 1 :
           #         print("flag 111")
           #         elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
           #                               body=relaventData)
           #     if flag1 == 0:
           #         print("flag 000")
           #         relaventData['KeywordSearched'] = relaventData['KeywordSearched'].pop(globalKeyword)
           #         elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
           #                                   body=relaventData)
           # If the list of data don't contain keyword search
       elif globalKeyword not in  relaventData['KeywordSearched'] :
           if flag1 == 1:
               print("flag 1111")
               relaventData['KeywordSearched']=relaventData['KeywordSearched'].replace('',globalKeyword)
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 == 0:
               print(flag)
               print("flag 0000")
               relaventData['KeywordSearched'] = relaventData['KeywordSearched'].replace(globalKeyword,'')
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
       else:
           elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)

           # This are the conditions to get update proper User in column of Most Relevant, to elastic search
           # If no data in column
       if relaventData['MostRelevantResponses'] == '':
           print(flag)
           if flag1 == 1:
               print("flag 1")
               relaventData['MostRelevantResponses']=user
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 == 0:
               print("flag 0")
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
           # If list of data contain only one element which is similar to the current user
       elif user in relaventData['MostRelevantResponses']:
           print(flag)
           if flag1 == 1:
               print("flag 11")
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 == 0:
               print("flag 00")
               relaventData['MostRelevantResponses'] = relaventData['MostRelevantResponses'].replace(user,'')
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
           # If list of data contains the current user
           # elif user in relaventData['MostRelevantResponses']:
           #     print(flag1)
           #     if flag1 == 1:
           #         print("flag 111")
           #         elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
           #                               body=relaventData)
           #     if flag1 == 0:
           #         print("flag 000")
           #         relaventData['MostRelevantResponses'] = relaventData['MostRelevantResponses'].pop(user)
           #         elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
           #                                   body=relaventData)
           # If the list of data don't contain current user
       elif user not in relaventData['MostRelevantResponses']:
           print(flag1)
           if flag1 == 1:
               print("flag 1111")
               relaventData['MostRelevantResponses'] = relaventData['MostRelevantResponses'].replace(user)
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
           if flag1 ==0:
               print("flag 0000")
               relaventData['MostRelevantResponses'] = relaventData['MostRelevantResponses'].replace(globalKeyword,'')
               elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                             body=relaventData)
       else:
           print(flag1)
           print("flag 10")
           elasticSearchObject.index(index='security_questionnaire', doc_type='document', id=relaventId,
                                         body=relaventData)
   except:
       pass

   # Data is again Sorted for getting data after submiting most revelent
   for data in globalRequiredData:
       if user in data['MostRelevantResponses'] and globalKeyword in data['KeywordSearched']:
           sortedResponses = [data] + sortedResponses
       else:
           sortedResponses1 = sortedResponses1 + [data]
   for i in sortedResponses1:
       sortedResponses.append(i)

   # this global Data to be user in relevantResponses method
   globalRequiredData = sortedResponses

   context={'questionnaireResult': globalRequiredData,'policiesResult': globalPolicyResult,'keyword':globalKeyword,'user1':user}

   return render(request,'questionnaireApp/home.html',context)



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
                elasticSearchObject.delete(index='questionnaire', doc_type='document',
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

