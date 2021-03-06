from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import TagWithInfo, Search, RelevantResponseDatabase1, UserSessionDatabase, KeywordSearchedDatabase, \
    MostFavouredResponseHistoryDatabase, FileUploadReport, Image
from django.contrib import messages

# Global Variable

globalRelaventId = []
globalKeyword = ''
globalRequiredData = []
globalPolicyResult = []
globalMostRelevantResponses = []
globalKeywordSearch = []
globalTags = []
globalKeywordList = []
globalUserList = []
dataBaseList = []
globalFilterUser = ''

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


    if ":-" in str:
        getSearchedKeyword = ((str.split(':-', 1)[0]).replace("in@", "")).strip()
        if getSearchedKeyword in inSearchKeyword:
            keyword = (str.split(':-', 1)[1]).strip()

        elif getSearchedKeyword == 'Tags':
            tagname = (str.split(':-', 1)[1]).strip()

            return displayTagInformation(request, tagname)

    else:
        getSearchedKeyword = ""
        keyword = str

        # Declare Global Keywords within this function

    global globalKeyword
    global globalPolicyResult
    global globalRequiredData
    global globalMostRelevantResponses
    global globalKeywordSearch
    global globalUserList
    global dataBaseList
    global globalFilterUser

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
    allResponses = []
    userResponses = []

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
        print (questionnaireRequiredData)

        for a in range(len(questionnaireRequiredData)):
            questionnaireRequiredData[a].update({'ID': questionnaireRequiredId[a]})

        for data in questionnaireRequiredData:
            if userKeyword.lower() in data['MostRelevantResponses']:
                sortedResponses = [data] + sortedResponses
            else:
                sortedResponses1 = sortedResponses1 + [data]

        globalRequiredData = sortedResponses + sortedResponses1

        for data in questionnaireRequiredData:
            if globalKeyword.lower() in data['KeywordSearched']:
                allResponses = [data] + allResponses
        print ("all responses",allResponses)

        for i in dataBaseList:
            if i['user_Keyword'] == globalFilterUser:
                print ("if condition successful if user match",globalFilterUser)
                for data in questionnaireRequiredData:
                    if i['user_Keyword'].lower() in data['MostRelevantResponses']:
                        userResponses = [data] + userResponses
                    # print ("user responses under condition",userResponses)
                break

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
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))

        if getSearchedKeyword.casefold() == 'questionnaire':
            context = {'questionnaireResult': globalRequiredData, 'questionnaireId': questionnaireRequiredId,
                       "tagNameList": tagNameList, 'keyword': keyword, 'questionnaireActive': 'active',
                       'userKeyword': userKeyword.lower()}
            return render(request, 'questionnaireApp/home.html', context)
        elif getSearchedKeyword.casefold() == 'policies':
            context = {'policiesResult': policiesSearchResult, 'questionnaireId': questionnaireRequiredId,
                       "tagNameList": tagNameList, 'keyword': keyword, 'policyActive': 'active',
                       'userKeyword': userKeyword.lower()}
            return render(request, 'questionnaireApp/home.html', context)
        elif relevantSearch == 'mostRelevant':
            if globalFilterUser:
                print("user response")
                context = {'questionnaireResult': userResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),
                           'questionnaireActive': 'active'}
            else:
                print("all users")
                print (allResponses)
                context = {'questionnaireResult': allResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),
                           'questionnaireActive': 'active'}
            return render(request, 'questionnaireApp/favourite.html', context)
        else:
            context = {'questionnaireResult': globalRequiredData, 'policiesResult': policiesSearchResult,
                       'questionnaireId': questionnaireRequiredId, "tagNameList": tagNameList, 'keyword': keyword,
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
    global globalUserList
    global dataBaseList

    key_count = 0
    keywordList = []
    keywordList1 = []
    keywordList2 = []
    initialList = []
    globalInitialList = []
    dict1 = {}
    userDict = {}
    usernameList = []


    imgUsrDict = {}
    imageObjectDict = Image.objects.all()
    imgStr=""
    uniqueKey=[]
    for usr in imageObjectDict:
        word = (usr.userName).split()
        for x in word:
            imgStr = imgStr + x[0]

        import random
        random_number = random.randint(0, 16777215)
        hex_number = format(random_number, 'x')
        hex_number = '#' + hex_number

        keywordQuerySet = TagWithInfo.objects.filter(createdBy=usr.userName,flag=1)
        for keyTag in keywordQuerySet:
            uniqueKey.append(keyTag.tagName)
            uniqueKey = list(dict.fromkeys(uniqueKey))

        keywordQuerySet = TagWithInfo.objects.filter(updatedBy=usr.userName,flag=1)
        for keyTag in keywordQuerySet:
            uniqueKey.append(keyTag.tagName)
            uniqueKey = list(dict.fromkeys(uniqueKey))

        if len(uniqueKey) != 0 :
            imgUsrDict.update({usr.userName: {'alias': imgStr, 'colorCode': hex_number, 'keyData': uniqueKey}})

        imgStr=""
        uniqueKey = []
    print("------------>><<----------", imgUsrDict)

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
    retriveData = RelevantResponseDatabase1.objects.all().values()
    dataBaseList = list(retriveData)
    print("database list", dataBaseList)
    letterStr = ""
    # for usr in dataBaseList:
    #     word = (usr['db_user']).split()
    #     for x in word:
    #         imgStr = imgStr + x[0]
    print("Initials", letterStr)

    for i in dataBaseList:
        if i['count'] > 0:
            keywordList.append(i['keywordSearched'])
            usernameList.append(i['db_user'])
    # globalInitialList = list(dict.fromkeys(initialList))
    # print("initials",globalInitialList)
    for u in usernameList:
        word1 = u.split()
        for x in word1:
            letterStr = letterStr + x[0]
        userDict.update({u: letterStr})
        letterStr = ''
    print("user name dict", userDict)
    for u in usernameList:
        for i in dataBaseList:
            if u == i['db_user']:
                if i['count'] > 0:
                    keywordList1.append(i['keywordSearched'])
        keywordList2 = keywordList1
        keywordList1 = []
        import random
        random_number1 = random.randint(0, 16777215)
        hex_number1 = format(random_number1, 'x')
        hex_number1 = '#' + hex_number1
        print('-------------->>Color Code<<-----------', hex_number1)
        for key, value in userDict.items():
            if key == u:
                u = u.replace(" ", "-")
                dict1.update({u: {'alias': value, 'colorCode': hex_number1, 'keyData': keywordList2}})
    print(dict1)
    globalKeywordList = list(dict.fromkeys(keywordList))
    globalUserList = list(dict.fromkeys(usernameList))
    for charIndex in range(len(globalUserList)):
        globalUserList[charIndex] = globalUserList[charIndex].replace(" ", "-")



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
                   'globalKeywordList': globalKeywordList,'globalUserList': globalUserList, 'dict1': dict1,'imgUsrDict':imgUsrDict}
        return render(request, 'questionnaireApp/index.html', context)
    except:
        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,
                   'globalKeywordList': globalKeywordList,'globalUserList': globalUserList, 'dict1': dict1,'imgUsrDict':imgUsrDict}
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

    relevantDataFromDb = RelevantResponseDatabase1.objects.all()
    flag = False

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
            # after work of Id is done of comparision so to get correct records, it is deleted
            # relaventData.pop('ID')
        # if isinstance(relaventData['MostRelevantResponses'], str):  # check if data type is string
        if relaventData['MostRelevantResponses'] == '':
            relaventData['MostRelevantResponses'] = [userKeyword.lower()]
            relaventData['KeywordSearched'] = [globalKeyword.lower()]
            elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                      body=relaventData)
            for data in relevantDataFromDb:
                if data.user_Keyword == userKeyword.lower():
                    flag = True
                    data.count += 1
                    data.save()
                    break

            if not flag:
                relevantDataFromDb = RelevantResponseDatabase1(user_Keyword=userKeyword.lower(), count=1,
                                                                   keywordSearched=globalKeyword, db_user=user)
                relevantDataFromDb.save()

        else:
            if relaventData['MostRelevantResponses'] == []:  # check empty list
                relaventData['MostRelevantResponses'] = [userKeyword.lower()]
                relaventData['KeywordSearched'] = [globalKeyword.lower()]
                elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)
                for data in relevantDataFromDb:
                    if data.user_Keyword == userKeyword.lower():
                        flag = True
                        data.count += 1
                        data.save()
                        break

                if not flag:
                    relevantDataFromDb = RelevantResponseDatabase1(user_Keyword=userKeyword.lower(), count=1,
                                                                   keywordSearched=globalKeyword, db_user=user)
                    relevantDataFromDb.save()
            else:
                if userKeyword.lower() in relaventData['MostRelevantResponses']:
                    print("to delete")
                    relaventData['MostRelevantResponses'].remove(userKeyword.lower())
                    relaventData['KeywordSearched'].remove(globalKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if data.user_Keyword == userKeyword.lower():
                            flag = True
                            data.count -= 1
                            data.save()
                            break

                    if not flag:
                        relevantDataFromDb = RelevantResponseDatabase1(user_Keyword=userKeyword.lower(), count=1,
                                                                       keywordSearched=globalKeyword,
                                                                       db_user=user)
                        relevantDataFromDb.save()

                else:
                    relaventData['MostRelevantResponses'].append(userKeyword.lower())
                    relaventData['KeywordSearched'].append(globalKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if data.user_Keyword == userKeyword.lower():
                            flag = True
                            data.count += 1
                            data.save()
                            break

                    if not flag:
                        relevantDataFromDb = RelevantResponseDatabase1(user_Keyword=userKeyword.lower(), count=1,
                                                                       keywordSearched=globalKeyword,
                                                                       db_user=user)
                        relevantDataFromDb.save()

        for data in globalRequiredData:
            if userKeyword.lower() in data['MostRelevantResponses']:
                sortedResponses = [data] + sortedResponses
            else:
                sortedResponses1 = sortedResponses1 + [data]

    except:
        pass

    # this global Data to be user in relevantResponses method
    globalRequiredData = sortedResponses + sortedResponses1

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult, 'keyword': globalKeyword,
               'userKeyword': userKeyword.lower(), "questionnaireActive": 'active'}

    return render(request, 'questionnaireApp/home.html', context)


def recentSearchKeyword(request, recentSearch):
    toLowerStr = ''
    if request.POST.get('mostRelevant') == 'mostRelevant':
        global globalFilterUser
        print ("mostrelevant for user", globalFilterUser)
        filterUser = request.POST.getlist('userFilter[]')
        for i in filterUser:
            toStr=str(i)
            replacedStr=toStr.replace('-',' ')
            toLowerStr=replacedStr.lower()
        globalFilterUser = toLowerStr
        return searchKeyword(request,recentSearch,relevantSearch='mostRelevant')
    elif request.GET.get('name') == 'mostRelevant':
        print (" mostrelevant for all")
        return searchKeyword(request, recentSearch, relevantSearch='mostRelevant')
    else:
        print ("else part")
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
            return render(request, "questionnaireApp/uploadFile.html", context)
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
