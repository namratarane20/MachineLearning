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
from .models import TagsInformation

userName = ''

# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    # global userName
    # userName = request.user.get_full_name()
    # print(userName)
    return dispalyTagName(request)


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
    allTagNameColoumn = TagsInformation.objects.all()
    for tags in allTagNameColoumn:
        tagNameList.append(tags.tagName)
        tagNameList = list(dict.fromkeys(tagNameList))
    # print('mydata type ',type(questionnaireRequiredData))

    context = {'questionnaireResult': questionnaireRequiredData,
               'questionnaireVendorNameSet': questionnnaireVendorNameSet, 'policiesResult': policiesSearchResult,
               'questionnaireId': questionnaireRequiredId, 'quelist1': queList, "tagNameList":tagNameList}

    return render(request, 'questionnaireApp/home.html', context, queList)


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


def toHomePage(request):
    return dispalyTagName(request)

def addToTags(request):

    global globalTags

    checkBoxList = request.POST.getlist('tagCheckbox[]')
    # addedtags = globalTags[int(checkBoxList) - 1]
    # print(globalTags)
    col1 = ""
    col2 = ""
    col3 = ""
    col4 = ""
    col5 = ""
    col6 = ""
    global userName
    userName = request.user.get_full_name()
    print(userName)
    tagsList = []
    tagname = request.POST['tagname']
    tagDescription = request.POST['tagDescription']
    # existingTagName = request.POST['existingTagName']
    # print(existingTagName)
    # print(tagname)
    try:
        for eachTagRow in checkBoxList:
            addedTags = globalTags[int(eachTagRow) - 1]
            # print("added tags : ", addedTags)
            # print("type : ", type(addedTags))
            tagsList.append(addedTags)
            print("list : ", tagsList)
            # print(type(tagsList))

        for dictData in tagsList:
            for coloumnName, rowData in dictData.items():
                print(coloumnName, rowData)
                if coloumnName == 'VendorName':
                    # questionnaireObj = Questionnaire(vendorname=rowData)
                    col1 = rowData
                elif coloumnName == 'SectionName':
                    # questionnaireObj = Questionnaire(sectionname=rowData)
                    col2 = rowData
                elif coloumnName == 'ControlName':
                    # questionnaireObj = Questionnaire(controlname=rowData)
                    col3 = rowData
                elif coloumnName == 'SecurityQuestions':
                    # questionnaireObj = Questionnaire(securityquestion=rowData)
                    col4 = rowData
                elif coloumnName == 'ServiceSolutionResponse':
                    # questionnaireObj = Questionnaire(response=rowData)
                    col5 = rowData
                elif coloumnName == 'ServiceSolutionComments':
                    # questionnaireObj = Questionnaire(additionalcomment=rowData)
                    col6 = rowData
                elif  request.POST['tagname']:
                    tagname =request.POST['tagname']
                # elif request.POST['existingTagName']:
                #     tagname = request.POST['existingTagName']
                elif request.POST['tagDescription']:
                    tagDescription= request.POST['tagDescription']
                    print('this is exsiting tag name===',tagname)
                elif userName is not None :
                    # userName= loggedUserName
                    print('logged user',userName)




            questionnaireObj = TagsInformation(vendorname=col1, sectionname=col2, controlname=col3,
                                             securityquestion=col4, response=col5, additionalcomment=col6,tagName=tagname, tagDescription= tagDescription,userName= userName)
            questionnaireObj.tagDescription = request.POST['tagDescription']

            questionnaireObj.save()

        print('data saved succesfully ')



        return dispalyTagName(request)
        # return render(request, 'questionnaireApp/demo.html', {'tagNameList': tagNameList})
    except Exception as e:
        print("exception occured : ", e)
        pass
        return render(request, 'questionnaireApp/home.html')


def dispalyTagName(request):
    # userName =request.user.get_full_name()
    # print('display at tags',userName)
    tagNameList = []
    allTagNameColoumn = TagsInformation.objects.all()
    for tags in allTagNameColoumn:
        tagNameList.append(tags.tagName)
        tagNameList = list(dict.fromkeys(tagNameList))
        # tagNameList = list(dict.fromkeys(tagNameList)) // this is for to remove duplicates from list which tag list

        print(tagNameList)

    print('this is tag name list', tagNameList)

    return render(request, 'questionnaireApp/demo.html', {'tagNameList': tagNameList,'userName':userName})


def displayTagInformation(request, tagname):
    print("selected tag name : ", tagname)
    databaseTags = TagsInformation.objects.filter(tagName = tagname).values()
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
        tagDesc.append(tagDescription.get("tagDescription"))

        print('this is previous description',tagDesc)
        print(type(tagDesc))



    # for savedTagName in addedTagdata:
    #     for databaseColName, databaseTagRow in savedTagName.items():
    #         print(databaseColName)
    #         print(databaseTagRow)

    # database= QuestionnaireTags.objects.values(tagName = tagname)
    # print(database)
    # print(type(database))
    return render(request, "questionnaireApp/TagTable.html", {'addedTagdata': addedTagdata, 'selectedTagName':tagname,'tagDesc':tagDesc})
# def destroyTagData(request):
#     TagsInformation.objects.all
#
#
#
#         return render(request, 'questionnaireApp/demo.html')


# tags = QuestionnaireTags.objects.all()
# listdata= []
# for x in tags:
#     listdata.append(x.vendorname + ' ' + x.sectionname + ' ' +x.controlname+ ''+x.securityquestion + ' ' + x.response + ' ' +x.additionalcomment+''+x.tagName)
#     print(listdata)
#     print(type(listdata))
# # return name_list
