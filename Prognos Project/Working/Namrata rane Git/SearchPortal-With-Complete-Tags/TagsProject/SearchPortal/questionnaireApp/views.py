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
from .forms import UserForm, ProfileForm
from .models import TagWithInfo
import datetime
# userName = ''

# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    # global userName
    # userName = request.user.get_full_name()
    # print(userName)
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
    print("inside search keyword")
    # This is a list which get the values of checkboxe
    global globalTags
    keyword = request.POST['keyword']
    queList = request.POST.getlist('questionChecked[]')
    # print (queList)
    check_list = request.POST.getlist('check[]')
    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    questionnaireSearchResult = elasticSearchObject.search(index="question_naire",
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
    questionnaireRequiredId = set({})

    for hit in questionnaireSearchResult['hits']['hits']:
        questionnaireRequiredData.append(hit['_source'])  # extracting required data
        questionnnaireVendorNameSet.add(hit['_source']['VendorName'])
        questionnaireRequiredId.add(hit['_id'])
    globalTags = questionnaireRequiredData

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

    tagNameList = []
    allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
    for tags in allTagNameColoumn:
        tagNameList.append(tags.tagName)
        tagNameList = list(dict.fromkeys(tagNameList))

    # print('mydata type ',type(questionnaireRequiredData))

    context = {'questionnaireResult': questionnaireRequiredData,
               'questionnaireVendorNameSet': questionnnaireVendorNameSet, 'policiesResult': policiesSearchResult,
               'questionnaireId': questionnaireRequiredId, 'quelist1': queList, "tagNameList":tagNameList,'keyword':keyword}

    return render(request, 'questionnaireApp/home.html', context, queList)


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
    return addToTags(request)

def addToTags(request):

    global globalTags

    # tagNameAndUsernameDict = {}
    dateUserTagDict = {}
    tempDict ={}

    checkBoxList = request.POST.getlist('tagCheckbox[]')
    # print('my checked list',checkBoxList)
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
            # print('data list ========',tagsList)
        for data in tagsList:
                col1 = data['VendorName']
                col2 = data['SectionName']
                col3 = data['ControlName']
                col4 = data['SecurityQuestions']
                col5 = data['Responses']
                col6 = data['AdditionalComments']
                tagname = request.POST['tagname']
                print('taganame issss',tagname)
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

        # logic to pass tagname list

        tagNameList = []
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))
        print('this is my tagname list for front apge',tagNameList)
        # logic to pass tag name and user names as dict( keys and values)

        # allTagNameColoumn = TagWithInfo.objects.filter(flag=1).values()
        # allData = list(allTagNameColoumn)  # list of dict
        # print('my database data ---',allData)
        # for tagData in allData:
        #     tagnames = tagData['tagName']
        #     print('tagname',tagnames)
        #     usernames = tagData['userName']
        #     print('username ',usernames)
        #     databaseDates = tagData['dateTime']
        #     print('date ',databaseDates)
        #     dateUserTagDict.update({tagnames:{usernames:databaseDates}})
        #
        # print('my dict is ======', dateUserTagDict)






        return render(request, 'questionnaireApp/demo.html', {'tagNameList':tagNameList})
    except Exception as e:
         print("exception occured here : ", e)
        # # pass
         return render(request, 'questionnaireApp/demo.html',{'tagNameList':tagNameList})


def displayTagInformation(request, tagname):
    print("selected tag name : ", tagname)
    databaseTags = TagWithInfo.objects.filter(tagName = tagname).values()
    # print('new data',databaseTags)
    # print(type(databaseTags)) # // quesySet
    # databaseTags are filter data from database where tag name is available (tag name is getting from front end )
    addedTagdata= list(databaseTags)
    flagTags = []
    for tag in addedTagdata:
        if tag['flag'] == 1:
            flagTags.append(tag)
    print('my flag 1 data',flagTags, type(flagTags) )

    #
    # print(addedTagdata)
    # print(type(addedTagdata)) # this is list of dict data
    tagDesc =[]
    for tagDescription in flagTags:

        # print(tagDescription)
        # print(type(tagDescription))
        # tagDesc.append(tagDescription.get("tagDescription"))
        tagDesc = tagDescription.get("tagDescription")

        print('this is previous description',tagDesc)
        print(type(tagDesc))



    return render(request, "questionnaireApp/TagTable.html", {'addedTagdata': flagTags, 'selectedTagName':tagname,'tagDesc':tagDesc})


def destroyTagInformation(request):
    print('inside destroy function=======================')
    print(request.POST['destroyedTagName'])
    destroyedTagName = request.POST['destroyedTagName']
    destroyTagsData = TagWithInfo.objects.filter(tagName = destroyedTagName).update(flag = 0)
    flag0data = TagWithInfo.objects.filter(tagName = destroyedTagName ).values()
    print('data of destroyed tag =======',flag0data)
    return addToTags(request)
