from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import TagWithInfo, Search, RelevantResponseDatabase, UserSessionDatabase, KeywordSearchedDatabase, \
    MostFavouredResponseHistoryDatabase, FileUploadReport
from django.contrib import messages
from datetime import datetime

# Global Variables

globalRelaventId = []
globalKeyword = ''
globalRequiredData = []
globalPolicyResult = []
globalMostRelevantResponses = []
globalKeywordSearch = []
globalTags = []
globalKeywordList = []


# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    if request.user.get_full_name():
        UserSessionDatabase(userName=request.user.get_full_name()).save()
    return addToTags(request)
    # return render(request, 'questionnaireApp/home.html')


@login_required
@transaction.atomic
def Logout(request):
    if request.user.get_full_name():
        userSessionDatabaseObject = UserSessionDatabase.objects.filter(userName=request.user.get_full_name()).order_by(
            '-logout')[:1]
        userSessionDatabaseObject[0].save()
    logout(request)
    return HttpResponseRedirect('/')


# End of sign in functinality==========================================================================


# searching keyword in elasticsearch index
def searchKeyword(request, recentSearch=None, relevantSearch=None):
    inSearchKeyword = "Questionnaire Policies"

    if request.POST and recentSearch == None:
        str = request.POST['keyword']
    else:
        str = recentSearch

    print("=============================>", str)
    if ":-" in str:
        getSearchedKeyword = ((str.split(':-', 1)[0]).replace("in@", "")).strip()
        if getSearchedKeyword in inSearchKeyword:
            keyword = (str.split(':-', 1)[1]).strip()
            print("---->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", keyword)
            print("with keyword")
        elif getSearchedKeyword == 'Tags':
            tagname = (str.split(':-', 1)[1]).strip()
            print("the keyword ===>>>", tagname)
            return displayTagInformation(request, tagname)

    else:
        getSearchedKeyword = ""
        keyword = str
        print("----->>>>>>", keyword)
        print("without keyword")

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

    userKeyword = user + ' ' + keyword

    KeywordSearchedDatabase(userName=request.user.get_full_name(), keyword=keyword).save()

    globalKeyword = keyword
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
                                                                   # "match": {
                                                                   #     "SecurityQuestions": globalKeyword
                                                                   # }
                                                                   'bool': {
                                                                       'must': {
                                                                           'match': {
                                                                               "SecurityQuestions": keyword
                                                                           }
                                                                       },
                                                                       'should': [
                                                                           {
                                                                               'match': {
                                                                                   'Responses': keyword
                                                                               }
                                                                           },
                                                                           {
                                                                               'match': {
                                                                                   'AdditionalComments': keyword
                                                                               }
                                                                           }
                                                                       ]
                                                                   }
                                                               }
                                                           },
                                                           request_timeout=30)

    if questionnaireSearchResult['hits']['hits']:

        # @@Piyush Jiwnae@@ code to count most searched keyword and recently searched keyword
        addToTags(request, str)
        # @@Piyush Jiwnae@@

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

        for a in range(len(questionnaireRequiredData)):
            questionnaireRequiredData[a].update({'ID': questionnaireRequiredId[a]})

        for data in questionnaireRequiredData:
            if userKeyword.lower() in data['MostRelevantResponses']:
                sortedResponses = [data] + sortedResponses
            else:
                sortedResponses1 = sortedResponses1 + [data]

        globalRequiredData = sortedResponses + sortedResponses1

        policiesResultList = elasticSearchObject.search(index='policies',
                                                        size=9999,
                                                        body={
                                                            'query': {
                                                                'match': {
                                                                    'Data': globalKeyword
                                                                }
                                                            }
                                                        })

        index = 0

        for hit in policiesResultList['hits']['hits']:
            if keyword.lower() in hit['_source']['Data'].lower():
                policiesSearchResult.append(hit['_source'])
                data = policiesSearchResult[index]['Data']
                nextLineCharIndex = len(data) - (
                    data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
                nextLineCharNextIndex = data.find("\n", nextLineCharIndex)
                upperCaseData = ''

                while True:
                    if data[nextLineCharIndex:nextLineCharNextIndex].isupper():
                        upperCaseData = data[nextLineCharIndex:nextLineCharNextIndex]
                        data = data[nextLineCharNextIndex:]
                        nextLineCharIndex = len(data) - (
                            data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
                        nextLineCharNextIndex = data.find("\n", nextLineCharIndex)
                    else:
                        break

                if keyword.lower() in data[nextLineCharIndex:nextLineCharNextIndex].lower():
                    policiesSearchResult[index]['Data'] = data[nextLineCharIndex:nextLineCharNextIndex]
                else:
                    policiesSearchResult[index]['Data'] = upperCaseData
                index += 1

        globalPolicyResult = policiesSearchResult
        tagNameList = []
        tagAndDescDict = {}
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagAndDescDict.update({tags.tagName: tags.tagDescription})

        if getSearchedKeyword.casefold() == 'questionnaire':
            context = {'questionnaireResult': globalRequiredData, 'questionnaireId': questionnaireRequiredId,
                       "tagAndDescDict": tagAndDescDict, 'keyword': keyword, 'questionnaireActive': 'active',
                       'userKeyword': userKeyword.lower()}
        elif getSearchedKeyword.casefold() == 'policies':
            context = {'policiesResult': policiesSearchResult, 'questionnaireId': questionnaireRequiredId,
                       "tagAndDescDict": tagAndDescDict, 'keyword': keyword, 'policyActive': 'active',
                       'userKeyword': userKeyword.lower()}
        elif relevantSearch == 'mostRelevant':
            context = {'questionnaireResult': sortedResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),
                       'questionnaireActive': 'active'}

        else:
            context = {'questionnaireResult': globalRequiredData, 'policiesResult': policiesSearchResult,
                       'questionnaireId': questionnaireRequiredId, "tagAndDescDict": tagAndDescDict, 'keyword': keyword,
                       'questionnaireActive': 'active', 'userKeyword': userKeyword.lower()}

        return render(request, 'questionnaireApp/home.html', context)

    else:
        messages.success(request, "Data not available for " + keyword + " keyword.")
        return addToTags(request)


def addToTags(request, str=None):
    global globalKeyword
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2
    userKeyword = user + ' ' + globalKeyword
    global globalRequiredData
    key_count = 0
    keywordList = []

    searchTable = Search.objects.all()
    if str:
        if ":-" in str:
            getSearchedKeyword = ((str.split(':-', 1)[0]).replace("in@", "")).strip()
            getKeyword = (str.split(':-', 1)[1]).casefold().strip()
            for s in searchTable:
                if (s.keyword == getKeyword):
                    key_count = 1
                    s.count = s.count + 1
                    s.save()
            if (key_count == 0):
                st = Search()
                st.keyword = getKeyword
                st.count = 1
                st.save()

        else:
            for s in searchTable:
                if (s.keyword == str):
                    key_count = 1
                    s.count = s.count + 1
                    s.save()
            if (key_count == 0):
                st = Search()
                st.keyword = str
                st.count = 1
                st.save()

    nst = Search.objects.all()
    newSearchTable = nst.order_by('-count')[:6]
    order = nst.order_by('-updated_at')[:6]

    # Logic for Most Relevant Response
    global globalKeywordList
    retriveData = RelevantResponseDatabase.objects.all().values()
    dataBaseList = list(retriveData)
    for i in dataBaseList:
        if user in i['userKeyword']:
            if i['count'] > 0:
                keywordList.append(i['keywordSearched'])
    globalKeywordList = keywordList

    checkBoxList = request.POST.getlist('tagCheckbox[]')
    global userName
    userName = request.user.get_full_name()
    tagsList = []  # to add all dict means all selected rows in list to make list of dict.
    try:
        for eachTagRow in checkBoxList:
            addedTags = globalRequiredData[int(eachTagRow) - 1]
            tagsList.append(addedTags)
        for data in tagsList:
            col1 = data['VendorName']
            col2 = data['SectionName']
            col3 = data['ControlName']
            col4 = data['SecurityQuestions']
            col5 = data['Responses']
            col6 = data['AdditionalComments']
            tagname = request.POST['tagname']
            tagNameWithOutSpaces = tagname.strip()  # "strip" ==> to remove left and right side spaces from tagName(which is str)
            tagDesc = request.POST['tagDescription']
            if tagDesc == '':
                tagDescQuerySet = TagWithInfo.objects.filter(tagName=tagNameWithOutSpaces).values()

                tagDescList = list(tagDescQuerySet)
                for tagDescription in tagDescList:
                    tagDesc = tagDescription.get("tagDescription")
            else:
                tagDesc = request.POST['tagDescription']

            dataBase = TagWithInfo.objects.all().order_by('-dateTime').values()
            addTodatabaseList = list(dataBase)
            flag = False
            for addToDb in addTodatabaseList:
                if col1 == addToDb['vendorname'] and col2 == addToDb.get('sectionname') and col3 == addToDb.get(
                        'controlname') and col4 == addToDb.get('securityquestion') and col5 == addToDb.get(
                    'response') and col6 == addToDb.get('additionalcomment') and tagNameWithOutSpaces == addToDb.get(
                    'tagName'):
                    if addToDb.get('flag') == 1:
                        flag = True
                    else:
                        flag = False
                    break

            if not flag:
                updatingTag = False  # if tagname already exists that means tag is updating and set it to True
                creatingTag = False  # if tagname does not exists that means tag is creating and set it to True

                if TagWithInfo.objects.filter(tagName=tagname).count() > 0:  # check if tagname already exists
                    tagsDbObject = TagWithInfo.objects.filter(tagName=tagname).order_by('-dateTime')
                    tagCreatedBy = tagsDbObject[0].createdBy  # get name of user who created the tag
                    updatingTag = True
                else:
                    creatingTag = True

                if creatingTag:
                    TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3, securityquestion=col4,
                                response=col5,
                                additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                                createdBy=userName).save()
                elif updatingTag:
                    TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3, securityquestion=col4,
                                response=col5,
                                additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                                createdBy=tagCreatedBy, updatedBy=userName).save()

        # logic to pass tagname list
        tagNameList = []
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))

        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,
                   'globalKeywordList': globalKeywordList}
        return render(request, 'questionnaireApp/index.html', context)
    except:
        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,
                   'globalKeywordList': globalKeywordList}
        return render(request, 'questionnaireApp/index.html', context)


def relevantResponses(request):
    # Fetch list of records to be most favourite through checkboxes
    fevButton = request.POST.getlist('fevButton[]')
    global globalKeyword
    global globalPolicyResult
    global globalRequiredData
    global globalKeywordSearch
    global globalMostRelevantResponses

    # Fetch user from SSO
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2

    userKeyword = user + ' ' + globalKeyword

    sortedResponses = []
    sortedResponses1 = []
    keywordList = []

    relevantDataFromDb = RelevantResponseDatabase.objects.all()
    flag = False

    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    try:
        # This is a loop to perform operation on selected records to be most favourite
        for id in fevButton:
            relaventData = globalRequiredData[int(id) - 1]
            relaventId = relaventData.get('ID')

        makeFavourite = False
        # if isinstance(relaventData['MostRelevantResponses'], str):  # check if data type is string
        if relaventData['MostRelevantResponses'] == '':
            relaventData['MostRelevantResponses'] = [userKeyword.lower()]
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                      body=relaventData)
            for data in relevantDataFromDb:
                if userKeyword == data.userKeyword:
                    flag = True
                    data.count += 1
                    data.keywordSearched = globalKeyword
                    data.userKeyword = userKeyword
                    data.save()
                    break
            if not flag:
                relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1,
                                                              keywordSearched=globalKeyword)
                relevantDataFromDb.save()
            makeFavourite = True
        else:
            if relaventData['MostRelevantResponses'] == []:  # check empty list
                relaventData['MostRelevantResponses'] = [userKeyword.lower()]
                elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)
                for data in relevantDataFromDb:
                    if userKeyword == data.userKeyword:
                        flag = True
                        data.count += 1
                        data.keywordSearched = globalKeyword
                        data.userKeyword = userKeyword
                        data.save()
                        break
                if not flag:
                    relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1,
                                                                  keywordSearched=globalKeyword)
                    relevantDataFromDb.save()
                makeFavourite = True

            else:
                if userKeyword.lower() in relaventData['MostRelevantResponses']:
                    relaventData['MostRelevantResponses'].remove(userKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if userKeyword == data.userKeyword:
                            flag = True
                            data.count -= 1
                            data.keywordSearched = globalKeyword
                            data.userKeyword = userKeyword
                            data.save()
                            break
                    if not flag:
                        relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1,
                                                                      keywordSearched=globalKeyword)
                        relevantDataFromDb.save()
                    makeFavourite = False

                else:
                    relaventData['MostRelevantResponses'].append(userKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if userKeyword == data.userKeyword:
                            flag = True
                            data.count += 1
                            data.keywordSearched = globalKeyword
                            data.userKeyword = userKeyword
                            data.save()
                            break
                    if not flag:
                        relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1,
                                                                      keywordSearched=globalKeyword)
                        relevantDataFromDb.save()
                    makeFavourite = True

        if makeFavourite:
            MostFavouredResponseHistoryDatabase(userName=request.user.get_full_name(),
                                                vendorName=relaventData['VendorName'],
                                                question=relaventData['SecurityQuestions'],
                                                response=relaventData['Responses'],
                                                additionalComment=relaventData['AdditionalComments'],
                                                status='Favourite', keyword=globalKeyword).save()
        else:
            MostFavouredResponseHistoryDatabase(userName=request.user.get_full_name(),
                                                vendorName=relaventData['VendorName'],
                                                question=relaventData['SecurityQuestions'],
                                                response=relaventData['Responses'],
                                                additionalComment=relaventData['AdditionalComments'],
                                                status='Unfavoured', keyword=globalKeyword).save()

        for data in globalRequiredData:
            if userKeyword.lower() in data['MostRelevantResponses']:
                sortedResponses = [data] + sortedResponses
            else:
                sortedResponses1 = sortedResponses1 + [data]
        for data in sortedResponses1:
            sortedResponses.append(data)

    except:
        pass

    # this global Data to be user in relevantResponses method
    globalRequiredData = sortedResponses

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult,
               'keyword': globalKeyword,
               'userKeyword': userKeyword.lower(), "questionnaireActive": 'active'}

    return render(request, 'questionnaireApp/home.html', context)


def recentSearchKeyword(request, recentSearch):
    if request.GET.get('name') == 'mostRelevant':
        return searchKeyword(request, recentSearch, relevantSearch='mostRelevant')
    else:
        return searchKeyword(request, recentSearch)


def indexQuestionnaireFile(request):
    from elasticsearch import Elasticsearch
    import csv
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    elasticSearchObject.indices.create(index='question_naire', ignore=400)  # creating index, ignore if already exists

    for csvFile in request.FILES.getlist('questionnaireFile'):
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

        # for row in reader:
        #     print("type : ", type(row))
        #     print("data : ", type(row['VendorName']))
        #     row['date'] = request.POST['questionnaireReceivedDate']
        #     print("row : ", row)

        try:
            fileUploadObject = FileUploadReport.objects.get(fileName=str(csvFile))
            fileUploadObject.noOfRows = indexCounter
            fileUploadObject.updatedBy = request.user.get_full_name()
            fileUploadObject.save()
        except:
            FileUploadReport(uploadedBy=request.user.get_full_name(), fileName=str(csvFile),
                             noOfRows=indexCounter - 1).save()

    messages.success(request, "Questionnaire File Successfully Uploaded")

    fileNameList = list(FileUploadReport.objects.all().values())
    context = {"fileNameList": fileNameList}
    return render(request, 'questionnaireApp/uploadFile.html', context)


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

        try:
            fileUploadObject = FileUploadReport.objects.get(fileName=str(fileName))
            fileUploadObject.updatedBy = request.user.get_full_name()
            fileUploadObject.save()
        except:
            FileUploadReport(uploadedBy=request.user.get_full_name(), fileName=str(fileName), noOfRows=1).save()

    messages.success(request, "Policy File Successfully Uploaded")
    fileNameList = list(FileUploadReport.objects.all().values())
    context = {"fileNameList": fileNameList}
    return render(request, 'questionnaireApp/uploadFile.html', context)


def adminLogin(request):
    return render(request, "questionnaireApp/adminLogin.html")


def adminMailVerification(request):
    emailId = 'admin@prognoshealth.com'
    password = 'admin@321'
    if emailId == request.POST['emailId']:
        if password == request.POST['password']:
            fileNameList = list(FileUploadReport.objects.all().values())
            context = {"fileNameList": fileNameList}
            return render(request, "questionnaireApp/adminHomePage.html", context)
        else:
            message = 'please enter valid password'
            return render(request, "questionnaireApp/adminLogin.html", {'message': message})
    else:
        message = 'please enter valid Email ID'
        return render(request, "questionnaireApp/adminLogin.html", {'message': message})


def toHomePage(request):
    return addToTags(request)


def displayTagInformation(request, tagname=None):
    databaseTags = TagWithInfo.objects.filter(tagName=tagname).values()

    if databaseTags:
        addedTagdata = list(databaseTags)
        flagTags = []
        for tag in addedTagdata:
            if tag['flag'] == 1:
                flagTags.append(tag)

        tagDesc = []
        for tagDescription in flagTags:
            tagDesc = tagDescription.get("tagDescription")

        return render(request, "questionnaireApp/TagTable.html",
                      {'addedTagdata': flagTags, 'selectedTagName': tagname, 'tagDesc': tagDesc})
    else:
        # messages = 'Data related to tag'+tagname+'is not available in the Database, please search for the correct Tag Name'
        messages.success(request,
                         'Data related to tag ' + tagname + ' is not available in the Database, please search for the correct Tag Name')
        return addToTags(request)


def destroyTagInformation(request):
    destroyedTagName = request.POST['destroyedTagName']
    destroyTagsData = TagWithInfo.objects.filter(tagName=destroyedTagName).update(flag=0)
    tagsDbObject = TagWithInfo.objects.filter(tagName=destroyedTagName).order_by('-dateTime')
    TagWithInfo(tagName=tagsDbObject[0].tagName, tagDescription=tagsDbObject[0].tagDescription,
                createdBy=tagsDbObject[0].createdBy, updatedBy=tagsDbObject[0].updatedBy, flag=0,
                destroyedBY=request.user.get_full_name()).save()
    return addToTags(request)


def tagsAndFavouredResponse(request):
    try:
        if request.POST['saveTag'] == 'saveTag':
            return addToTags(request)
    except:
        try:
            if request.POST['fevButton[]']:
                return relevantResponses(request)
        except:
            pass


def uploadFile(request):
    try:
        fileUploadDatabaseList = list(FileUploadReport.objects.all().values())
        return render(request, "questionnaireApp/uploadFile.html", {"fileNameList": fileUploadDatabaseList})
    except:
        return render(request, "questionnaireApp/uploadFile.html")


def report(request):
    tagsInfoReportList = list(TagWithInfo.objects.all().order_by('-dateTime').values())

    favouritesReportList = list(MostFavouredResponseHistoryDatabase.objects.all().order_by('-time').values())

    userSessionDatabaseList = list(UserSessionDatabase.objects.all().order_by('-login').values())
    userSessionDatabaseList[0]['logout'] = ''  # because current logged in user's logout time should be empty

    keywordSearchedList = list(KeywordSearchedDatabase.objects.all().order_by('-time').values())

    fileUploadHistoryList = list(FileUploadReport.objects.all().order_by('-uploadedTime').values())

    context = {"tagsInfoList": tagsInfoReportList, "favouritesReportList": favouritesReportList,
               "userSessionDatabaseList": userSessionDatabaseList, "keywordSearchedList": keywordSearchedList,
               "fileUploadHistoryList": fileUploadHistoryList}
    return render(request, "questionnaireApp/historyReport.html", context)


def fillQuestionnaire(request, vendorName):
    context = {"vendor": vendorName}
    return render(request, "questionnaireApp/fillQuestionnaire.html", context)


def toAdminHomePage(request):
    return render(request, "questionnaireApp/adminHomePage.html")


def indexFilePage(request):
    return render(request, "questionnaireApp/uploadFile.html")


def uploadNewQuestionnaire(request):
    return render(request, "questionnaireApp/uploadNewQuestionnaire.html")
