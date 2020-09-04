from datetime import datetime
from operator import index

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import TagWithInfo, Search, RelevantResponseDatabase1, UserSessionDatabase, KeywordSearchedDatabase, \
    MostFavouredResponseHistoryDatabase, FileUploadReport, Image, AdminDB, QuestionDB
from django.contrib import messages
import re, os, csv, slack
from elasticsearch import Elasticsearch
import pandas as pd

# Global Variables

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
globalClientId = ""
imgUsrDict = {}
tagNameList = []
dict1 = {}
newSearchTable = []
order = []

elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

# function to implement login functionality with single sign on=================
@login_required
def Home(request):
    if request.user.get_full_name():
        UserSessionDatabase(userName=request.user.get_full_name()).save()
    return addToTags(request)


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

    questionnaireSearchResult = elasticSearchObject.search(index="question_naire",
                                                           size=9999,
                                                           body={
                                                               "query": {
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

        for data in questionnaireRequiredData:
            if globalKeyword.lower() in data['KeywordSearched']:
                allResponses = [data] + allResponses

        for i in dataBaseList:
            if i['user_Keyword'] == globalFilterUser:
                for data in questionnaireRequiredData:
                    if i['user_Keyword'].lower() in data['MostRelevantResponses']:
                        userResponses = [data] + userResponses
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
        tagAndDescDict = {}
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagAndDescDict.update({tags.tagName: tags.tagDescription})

        if getSearchedKeyword.casefold() == 'questionnaire':
            context = {'questionnaireResult': globalRequiredData, 'questionnaireId': questionnaireRequiredId,
                       "tagAndDescDict": tagAndDescDict, 'keyword': keyword, 'questionnaireActive': 'active',
                       'userKeyword': userKeyword.lower()}
            return render(request, 'questionnaireApp/home.html', context)
        elif getSearchedKeyword.casefold() == 'policies':
            context = {'policiesResult': policiesSearchResult, 'questionnaireId': questionnaireRequiredId,
                       "tagAndDescDict": tagAndDescDict, 'keyword': keyword, 'policyActive': 'active',
                       'userKeyword': userKeyword.lower()}
            return render(request, 'questionnaireApp/home.html', context)
        elif relevantSearch == 'mostRelevant':
            if globalFilterUser:
                context = {'questionnaireResult': userResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList': globalKeywordList,'dict1': dict1,'imgUsrDict': imgUsrDict,
                           'questionnaireActive': 'active'}
            else:
                context = {'questionnaireResult': allResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList': globalKeywordList,'dict1': dict1,'imgUsrDict': imgUsrDict,
                           'questionnaireActive': 'active'}
            return render(request, 'questionnaireApp/favourite.html', context)

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
    global globalUserList
    global dataBaseList
    global imgUsrDict
    global tagNameList
    global dict1
    global newSearchTable
    global order

    key_count = 0
    keywordList = []
    keywordList1 = []
    keywordList2 = []
    initialList = []
    globalInitialList = []

    userDict = {}
    usernameList = []

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
    newSearchTableList = nst.order_by('-count')[:5]
    newSearchTable = list(newSearchTableList)
    print("---->>newSearchTable<<----", newSearchTable)

    orderList = nst.order_by('-updated_at')[:5]
    order = list(orderList)
    print("------>>order<<---",order)
    # Logic for Most Relevant Response
    global globalKeywordList
    retriveData = RelevantResponseDatabase1.objects.all().values()
    dataBaseList = list(retriveData)
    letterStr = ""

    for i in dataBaseList:
        if i['count'] > 0:
            keywordList.append(i['keywordSearched'])
            usernameList.append(i['db_user'])

    for u in usernameList:
        word1 = u.split()
        for x in word1:
            letterStr = letterStr + x[0]
        userDict.update({u: letterStr})
        letterStr = ''

    for u in usernameList:
        for i in dataBaseList:
            if u == i['db_user']:
                if i['count'] > 0:
                    keywordList1.append(i['keywordSearched'])
        keywordList2 = keywordList1
        keywordList1 = []

        hex_number1 = colorCodeGenerator()

        for key, value in userDict.items():
            if key == u:
                u = u.replace(" ", "-")
                dict1.update({u: {'alias': value, 'colorCode': hex_number1, 'keyData': keywordList2}})

        print("----->>dict1<<------",dict1)
    globalKeywordList = list(dict.fromkeys(keywordList))
    print('-------->>globalKeywordList<<---',globalKeywordList)
    globalUserList = list(dict.fromkeys(usernameList))
    for charIndex in range(len(globalUserList)):
        globalUserList[charIndex] = globalUserList[charIndex].replace(" ", "-")

    # code to fetch vendors summary from database
    adminDbDataList = list(AdminDB.objects.filter(status=1).order_by('-receivedDate').values())

    vendorNameDictionary = {}
    for data in adminDbDataList:
        if data['receivedDate']:
            data['receivedDate'] = data['receivedDate'].date()
        if data['submittedDate']:
            data['submittedDate'] = data['submittedDate'].date()
        if data['vendorName'] in vendorNameDictionary.keys():
            vendorNameDictionary[data['vendorName']]['counter'] += 1
            vendorNameDictionary[data['vendorName']]['vendorData'].append(data)
        else:
            link = data['vendorName'].replace(" ", "-")
            dataList = []
            dataList.append(data)
            vendorNameDictionary[data['vendorName']] = {'link': link, 'counter': 1, 'vendorData': dataList}
    # vendors summary  fetched from database

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
            col2 = data['scope']
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
                if col1 == addToDb['vendorname'] and col2 == addToDb.get('sectionname') and col4 == addToDb.get('securityquestion') and col5 == addToDb.get(
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
                    TagWithInfo(vendorname=col1, sectionname=col2, securityquestion=col4,
                                response=col5,
                                additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                                createdBy=userName).save()
                elif updatingTag:
                    TagWithInfo(vendorname=col1, sectionname=col2, securityquestion=col4,
                                response=col5,
                                additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                                createdBy=tagCreatedBy, updatedBy=userName).save()

        # logic to pass tagname list

        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))

        print('--------->>tagNameList<<-------',tagNameList)

        imageObjectDict = Image.objects.all()
        imgStr = ""
        uniqueKey = []
        for usr in imageObjectDict:
            word = (usr.userName).split()
            for x in word:
                imgStr = imgStr + x[0]

            hex_number = colorCodeGenerator()

            keywordQuerySet = TagWithInfo.objects.filter(createdBy=usr.userName, flag=1)
            for keyTag in keywordQuerySet:
                uniqueKey.append(keyTag.tagName)
                uniqueKey = list(dict.fromkeys(uniqueKey))
            keywordQuerySet = TagWithInfo.objects.filter(updatedBy=usr.userName, flag=1)
            for keyTag in keywordQuerySet:
                uniqueKey.append(keyTag.tagName)
                uniqueKey = list(dict.fromkeys(uniqueKey))
            if len(uniqueKey) != 0:
                imgUsrDict.update({usr.userName: {'alias': imgStr, 'colorCode': hex_number, 'keyData': uniqueKey}})
            print("------>>imgUsrDict<<------",imgUsrDict)
            imgStr = ""
            uniqueKey = []

        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,
                   'globalKeywordList': globalKeywordList, 'globalUserList': globalUserList, 'dict1': dict1,
                   'imgUsrDict': imgUsrDict, 'adminDbDataList': adminDbDataList,
                   'vendorNameDictionary': vendorNameDictionary}
        return render(request, 'questionnaireApp/index.html', context)
    except:
        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,
                   'globalKeywordList': globalKeywordList, 'globalUserList': globalUserList, 'dict1': dict1,
                   'imgUsrDict': imgUsrDict, 'adminDbDataList': adminDbDataList,
                   'vendorNameDictionary': vendorNameDictionary}
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

    try:
        # This is a loop to perform operation on selected records to be most favourite
        for id in fevButton:
            relaventData = globalRequiredData[int(id) - 1]
            relaventId = relaventData.get('ID')

        makeFavourite = False
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
                    data.keywordSearched = globalKeyword
                    data.userKeyword = userKeyword
                    data.save()
                    break
            if not flag:
                relevantDataFromDb = RelevantResponseDatabase1(user_Keyword=userKeyword.lower(), count=1,
                                                               keywordSearched=globalKeyword, db_user=user)
                relevantDataFromDb.save()
            makeFavourite = True
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
                makeFavourite = True
            else:
                if userKeyword.lower() in relaventData['MostRelevantResponses']:
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
                    makeFavourite = False

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

    except:
        pass

    # this global Data to be user in relevantResponses method
    globalRequiredData = sortedResponses + sortedResponses1

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult,
               'keyword': globalKeyword,
               'userKeyword': userKeyword.lower(), "questionnaireActive": 'active'}

    return render(request, 'questionnaireApp/home.html', context)


def recentSearchKeyword(request):
    toLowerStr=""
    if request.method == 'POST':
        recentSearch = request.POST.get('mostRelevant')
        global globalFilterUser
        filterUser = request.POST.getlist('userFilter[]')
        for i in filterUser:
            toStr = str(i)
            replacedStr = toStr.replace('-', ' ')
            toLowerStr = replacedStr.lower()
        globalFilterUser = toLowerStr
        return searchKeyword(request, recentSearch,relevantSearch='mostRelevant')
    elif request.method == 'GET':
        recentSearch = request.GET.get('mostRelevant')
        return searchKeyword(request,recentSearch, relevantSearch='mostRelevant')


def recentSearched(request):
    if request.method == 'POST':
        recentSearch = request.POST.get('recentSearchedButton')
        return searchKeyword(request,recentSearch)


def indexQuestionnaireFile(request):
    elasticSearchObject.indices.create(index='question_naire', ignore=400)  # creating index, ignore if already exists
    for csvFile in request.FILES.getlist('questionnaireFile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file, encoding=request.encoding, errors='ignore')  # to get text file
        reader = csv.DictReader(file)  # reading csv
        vendorName = request.POST['vendorName']
        docLink = request.POST['questionnaireDocumentLink']
        scope = request.POST['questionnaireScope']
        submittedDate = request.POST['questionnaireSubmittedDate']
        receivedDate = request.POST['questionnaireReceivedDate']
        if request.POST['questionnaireSubmittedDate'] == '':
            clientId = vendorName + str(datetime.today().strftime('%Y-%m-%d'))
        else:
            clientId = vendorName + str(request.POST['questionnaireSubmittedDate'])
        indexCounter = 1
        for row in reader:
            row['clientId'] = clientId
            row['VendorName'] = vendorName
            row['scope'] = scope
            row['KeywordSearched'] = ''
            row['MostRelevantResponses'] = ''
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
        try:
            adminDbObject = AdminDB.objects.get(fileName=str(csvFile))
            if request.POST['questionnaireReceivedDate'] != '':
                adminDbObject.receivedDate = receivedDate
            if request.POST['questionnaireSubmittedDate'] != '':
                adminDbObject.submittedDate = submittedDate
            adminDbObject.relatedCommunication = request.POST['questionnaireRelatedCommunication']
            adminDbObject.clientId = clientId
            adminDbObject.documentLink = docLink
            adminDbObject.summary = scope
            adminDbObject.status = 1
            adminDbObject.save()
        except:
            if request.POST['questionnaireReceivedDate'] != '' and request.POST['questionnaireSubmittedDate'] != '':
                AdminDB(fileName=str(csvFile), vendorName=vendorName, submittedDate=submittedDate, status=1,
                        relatedCommunication=request.POST['questionnaireRelatedCommunication'],
                        clientId=clientId, summary=scope, documentLink=docLink,
                        receivedDate=receivedDate).save()
            elif request.POST['questionnaireSubmittedDate'] != '' and request.POST['questionnaireReceivedDate'] == '':
                AdminDB(fileName=str(csvFile), vendorName=vendorName, submittedDate=submittedDate, status=1,
                        relatedCommunication=request.POST['questionnaireRelatedCommunication'],
                        clientId=clientId, summary=scope, documentLink=docLink).save()
            elif request.POST['questionnaireReceivedDate'] != '' and request.POST['questionnaireSubmittedDate'] == '':
                AdminDB(fileName=str(csvFile), vendorName=vendorName, status=1,
                        relatedCommunication=request.POST['questionnaireRelatedCommunication'],
                        clientId=clientId, summary=scope, documentLink=docLink,
                        receivedDate=receivedDate).save()
            else:
                AdminDB(fileName=str(csvFile), vendorName=vendorName, status=1,
                        relatedCommunication=request.POST['questionnaireRelatedCommunication'],
                        clientId=clientId, summary=scope, documentLink=docLink).save()
    messages.success(request, "Questionnaire File Successfully Uploaded")
    fileUploadDatabaseList = list(FileUploadReport.objects.all().values())
    distinctVendors = AdminDB.objects.values('vendorName').distinct()
    context = {"fileNameList": fileUploadDatabaseList, 'distinctVendors': distinctVendors}
    return render(request, 'questionnaireApp/uploadFile.html', context)


def indexPoliciesFile(request):
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
            try:
                fileUploadDatabaseList = list(FileUploadReport.objects.all().values())
                distinctVendors = AdminDB.objects.values('vendorName').distinct()
                context = {"fileNameList": fileUploadDatabaseList, 'distinctVendors': distinctVendors}
                return render(request, "questionnaireApp/uploadFile.html", context)
            except:
                return render(request, "questionnaireApp/uploadFile.html")
        else:
            message = 'please enter valid password'
            return render(request, "questionnaireApp/adminLogin.html", {'message': message})
    else:
        message = 'please enter valid Email ID'
        return render(request, "questionnaireApp/adminLogin.html", {'message': message})


def toHomePage(request):
    return addToTags(request)


def displayTagInformation(request, tagname=None):
    if request.method == "GET":
        tagname = request.GET['tagsData']

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
                      {'addedTagdata': flagTags, 'selectedTagName': tagname, 'tagDesc': tagDesc,'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList': globalKeywordList,'dict1': dict1,'imgUsrDict': imgUsrDict,})
    else:
        # messages = 'Data related to tag'+tagname+'is not available in the Database, please search for the correct Tag Name'
        messages.success(request,
                         'Data related to tag ' + tagname + ' is not available in the Database, please search for the correct Tag Name')
        return addToTags(request)


def destroyTagInformation(request):
    global imgUsrDict
    global tagNameList

    destroyedTagName = request.POST['destroyedTagName']
    destroyTagsData = TagWithInfo.objects.filter(tagName=destroyedTagName).update(flag=0)
    tagNameList.remove(destroyedTagName)
    tagsDbObject = TagWithInfo.objects.filter(tagName=destroyedTagName).order_by('-dateTime')
    TagWithInfo(tagName=tagsDbObject[0].tagName, tagDescription=tagsDbObject[0].tagDescription,
                createdBy=tagsDbObject[0].createdBy, updatedBy=tagsDbObject[0].updatedBy, flag=0,
                destroyedBY=request.user.get_full_name()).save()
    imgUsrDict = {}
    tagNameList = []

    return addToTags(request)


def tagsAndFavouredResponse(request):
    try:
        if request.POST['saveTag'] == 'saveTag':
            print("calling add to tags")
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
        distinctVendors = AdminDB.objects.values('vendorName').distinct()
        context = {"fileNameList": fileUploadDatabaseList, 'distinctVendors': distinctVendors}
        return render(request, "questionnaireApp/uploadFile.html", context)
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


def colorCodeGenerator():
    colorCodeBool = True
    import random
    while colorCodeBool:
        random_number = random.randint(0, 16777215)
        hex_number = format(random_number, 'x')
        if len(hex_number) == 6:
            hex_number = '#' + hex_number
            return hex_number
        else:
            colorCodeGenerator()


def fillQuestionnaire(request, clientId):
    global globalClientId
    global particularVendorData
    questionaireData = []
    newQuestionnaireDataList1 = []
    newQuestionnaireDataList2 = []
    counter = 0
    checkedQuestion = ''
    fileName = ''
    systemPath = ''
    dowloadDataFrame = pd.DataFrame(columns=['Security Question', 'Response', 'Additional Comment'])

    if request.method == 'GET':
        if request.GET.get('name') == 'final':
            questionnaireSearchResult = elasticSearchObject.search(index="question_naire",
                                                                   size=9999,
                                                                   body={
                                                                       "query": {
                                                                           "match": {
                                                                               "clientId": clientId
                                                                           }
                                                                       }
                                                                   },
                                                                   request_timeout=30)

            questionnaireRequiredData = []  # data to be display in table
            vendorName = questionnaireSearchResult['hits']['hits'][0]['_source']['VendorName']

            for hit in questionnaireSearchResult['hits']['hits']:
                if hit['_source']['clientId'] == clientId:
                    questionnaireRequiredData.append(hit['_source'])  # extracting required data
            context = {"vendorName": vendorName, "vendorsData": questionnaireRequiredData,
                       "dataFromElasticsearch": True, "clientId": clientId}
        else:
            newQuestionnaireData = QuestionDB.objects.filter(admin__clientId=clientId)
            vendorName = AdminDB.objects.filter(clientId=clientId)[0].vendorName

            for object in newQuestionnaireData:
                responseKey = re.sub(r"\W", "", (object.question + str(object.id) + "response"))
                commentKey = re.sub(r"\W", "", (object.question + str(object.id) + "comment"))
                object.responseKey = responseKey
                object.commentKey = commentKey
                if object.exactmatch == 1:
                    newQuestionnaireDataList1.append(object)
                elif object.exactmatch == 0:
                    newQuestionnaireDataList2.append(object)
            questionaireData = newQuestionnaireDataList1 + newQuestionnaireDataList2
            particularVendorData = list(QuestionDB.objects.filter(admin__clientId=clientId))
            globalClientId = clientId

            # SLACK INTEGRATION CODE #
            client = slack.WebClient(token="xoxp-2151383821-740407775412-858683938353-2857f1f859025d59c6566ae8bfe28e0f")
            client_set = set({})
            for client_member in client.conversations_members(channel="CQHJ85FSS")['members']:
                client_set.add(client_member)
            user_set = set({})
            for user_list in client.users_list()['members']:
                for client_list_set in client_set:
                    if user_list['id'] == client_list_set:
                        user_set.add(user_list['name'])

            context = {"dataFromDatabase": True, 'vendorsData': questionaireData, "vendorName": vendorName,
                       'userSet': user_set, 'clientId': clientId}
    elif request.method == 'POST':
        try:
            if request.POST['save'] == 'save':
                for object in QuestionDB.objects.filter(admin__clientId=clientId):
                    responseKey = re.sub(r"\W", "", (object.question + str(object.id) + "response"))
                    commentKey = re.sub(r"\W", "", (object.question + str(object.id) + "comment"))
                    if request.POST[responseKey]:
                        object.response = request.POST[responseKey]
                    if request.POST[commentKey]:
                        object.additionalComment = request.POST[commentKey]
                    object.save()
                newQuestionnaireData = QuestionDB.objects.filter(admin__clientId=clientId)
                vendorName = AdminDB.objects.filter(clientId=clientId)[0].vendorName

                newQuestionnaireDataList1 = []
                newQuestionnaireDataList2 = []
                for object in newQuestionnaireData:
                    responseKey = re.sub(r"\W", "", (object.question + str(object.id) + "response"))
                    commentKey = re.sub(r"\W", "", (object.question + str(object.id) + "comment"))
                    object.responseKey = responseKey
                    object.commentKey = commentKey
                    if object.exactmatch == 1:
                        newQuestionnaireDataList1.append(object)
                    elif object.exactmatch == 0:
                        newQuestionnaireDataList2.append(object)
                questionaireData = newQuestionnaireDataList1 + newQuestionnaireDataList2
                particularVendorData = list(QuestionDB.objects.filter(admin__clientId=clientId))

                # SLACK INTEGRATION CODE #
                client = slack.WebClient(
                    token="xoxp-2151383821-740407775412-858683938353-2857f1f859025d59c6566ae8bfe28e0f")
                client_set = set({})
                for client_member in client.conversations_members(channel="CQHJ85FSS")['members']:
                    client_set.add(client_member)
                user_set = set({})
                for user_list in client.users_list()['members']:
                    for client_list_set in client_set:
                        if user_list['id'] == client_list_set:
                            user_set.add(user_list['name'])

                context = {"dataFromDatabase": True, 'vendorsData': questionaireData, "vendorName": vendorName,
                           'userSet': user_set, 'clientId': clientId}

        except:
            dataForDownload = QuestionDB.objects.filter(admin__clientId=clientId).values()
            listOfDataForDownload = list(dataForDownload)
            questionList = []
            responsesList = []
            commentList = []
            for downloadData in listOfDataForDownload:
                questionList.append(downloadData.get('question'))
                responsesList.append(downloadData.get('response'))
                commentList.append(downloadData.get('additionalComment'))
                dowloadDataFrame = pd.DataFrame(
                    {'Security Question': questionList, 'Response': responsesList, 'Additional Comment': commentList})
            vendorNameForFile = AdminDB.objects.filter(clientId=clientId)[0].vendorName
            adminDBData = AdminDB.objects.filter(vendorName=vendorNameForFile).values()
            listOfAdminDB = list(adminDBData)
            for fileNameForDownload in listOfAdminDB:
                fileName = fileNameForDownload.get('fileName')
                dumyPath = os.path.expanduser('~') + '\Downloads'
                systemPath = dumyPath + r'\''[:-1]

            try:
                if request.POST['csvDownload'] == 'csvDownload':
                    dowloadDataFrame.to_csv(systemPath + fileName, index=False)

            except:
                try:
                    if request.POST['excelDownload'] == 'excelDownload':
                        removedFileName = fileName[:-4]
                        dowloadDataFrame.to_excel(systemPath + removedFileName + '.xlsx', index=False)

                except Exception as e:
                    pass

            newQuestionnaireData = QuestionDB.objects.filter(admin__clientId=clientId)
            vendorName = AdminDB.objects.filter(clientId=clientId)[0].vendorName

            newQuestionnaireDataList1 = []
            newQuestionnaireDataList2 = []
            for object in newQuestionnaireData:
                responseKey = re.sub(r"\W", "", (object.question + str(object.id) + "response"))
                commentKey = re.sub(r"\W", "", (object.question + str(object.id) + "comment"))
                object.responseKey = responseKey
                object.commentKey = commentKey
                if object.exactmatch == 1:
                    newQuestionnaireDataList1.append(object)
                elif object.exactmatch == 0:
                    newQuestionnaireDataList2.append(object)
            questionaireData = newQuestionnaireDataList1 + newQuestionnaireDataList2

            # SLACK INTEGRATION CODE #
            client = slack.WebClient(token="xoxp-2151383821-740407775412-858683938353-2857f1f859025d59c6566ae8bfe28e0f")
            client_set = set({})
            for client_member in client.conversations_members(channel="CQHJ85FSS")['members']:
                client_set.add(client_member)
            user_set = set({})
            for user_list in client.users_list()['members']:
                for client_list_set in client_set:
                    if user_list['id'] == client_list_set:
                        user_set.add(user_list['name'])

            context = {"dataFromDatabase": True, 'vendorsData': questionaireData, "vendorName": vendorName,
                       'userSet': user_set, 'clientId': clientId}

    return render(request, "questionnaireApp/fillQuestionnaire.html", context)


def toAdminHomePage(request):
    adminDbDataList = list(AdminDB.objects.all().order_by('-receivedDate').values())
    newVendorsList = []
    oldVendorsList = []
    for data in adminDbDataList:
        if data['status'] == 0:
            newVendorsList.append(data)
        else:
            oldVendorsList.append(data)
    adminDbDataList = newVendorsList + oldVendorsList
    vendorNameDictionary = {}
    for data in adminDbDataList:
        if data['receivedDate']:
            data['receivedDate'] = data['receivedDate'].date()
        if data['submittedDate']:
            data['submittedDate'] = data['submittedDate'].date()
        if data['vendorName'] in vendorNameDictionary.keys():
            vendorNameDictionary[data['vendorName']]['counter'] += 1
            vendorNameDictionary[data['vendorName']]['vendorData'].append(data)
        else:
            link = data['vendorName'].replace(" ", "-")
            dataList = []
            dataList.append(data)
            vendorNameDictionary[data['vendorName']] = {'link': link, 'counter': 1, 'vendorData': dataList}
    context = {'adminDbDataList': adminDbDataList, 'vendorNameDictionary': vendorNameDictionary}
    return render(request, "questionnaireApp/adminHomePage.html", context)


def uploadNewQuestionnaire(request):
    fileUploadDatabaseList = AdminDB.objects.filter(status=0).order_by('-receivedDate')
    distinctVendors = AdminDB.objects.values('vendorName').distinct()
    context = {"fileNameList": fileUploadDatabaseList, 'distinctVendors': distinctVendors}
    return render(request, "questionnaireApp/uploadNewQuestionnaire.html", context)


def uploadNewQuestionnaireToDatabase(request):
    exactMatchQuestion = []
    import csv
    from elasticsearch import Elasticsearch

    for csvFile in request.FILES.getlist('questionnaireFile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file)  # to get text file
        reader = csv.DictReader(file)  # reading csv

        vendorName = request.POST['vendorName']
        if request.POST['questionnaireReceivedDate'] == '':
            receivedDate = datetime.today().strftime('%Y-%m-%d')
        else:
            receivedDate = request.POST['questionnaireReceivedDate']

        try:
            adminDbObject = AdminDB.objects.get(fileName=str(csvFile))
            QuestionDB.objects.filter(admin=adminDbObject).delete()
            adminDbObject.summary = request.POST['questionnaireSummary']
            adminDbObject.receivedDate = receivedDate
            adminDbObject.clientId = (vendorName + " " + receivedDate)
            adminDbObject.save()
        except:
            adminDbObject = AdminDB(vendorName=vendorName, summary=request.POST['questionnaireSummary'],
                                    receivedDate=receivedDate, fileName=str(csvFile), status=0,
                                    clientId=(vendorName + " " + receivedDate))
            adminDbObject.save()

        for row in reader:
            rowQuestion = row.get('SecurityQuestions')
            questionDBDAta = QuestionDB()
            questionDBDAta.admin = adminDbObject
            questionDBDAta.question = rowQuestion
            questionDBDAta.response = ''
            questionDBDAta.additionalComment = ''
            questionDBDAta.save()

            exactMatchQuestionResult = elasticSearchObject.search(index="question_naire",
                                                                  size=9999,
                                                                  body={
                                                                      "query": {
                                                                          'bool': {
                                                                              'must': [
                                                                                  {
                                                                                      'match': {
                                                                                          "VendorName": vendorName
                                                                                      }
                                                                                  },
                                                                                  {
                                                                                      'match': {
                                                                                          "SecurityQuestions": rowQuestion
                                                                                      }
                                                                                  }

                                                                              ]

                                                                          }
                                                                      }

                                                                  },
                                                                  request_timeout=30)
            if exactMatchQuestionResult['hits']['hits']:
                for hit in exactMatchQuestionResult['hits']['hits']:
                    exactMatchQuestion.append(hit['_source'])
                for i in exactMatchQuestion:
                    iResponse = i.get('Responses')
                    iQuestion = i.get('SecurityQuestions')
                    iComment = i.get('AdditionalComments')
                    if questionDBDAta.question == iQuestion:
                        questionDBDAta.question = rowQuestion
                        questionDBDAta.response = iResponse
                        questionDBDAta.additionalComment = iComment
                        questionDBDAta.exactmatch = 1
                        questionDBDAta.save()
            else:
                questionDBDAta.question == iQuestion
                questionDBDAta.exactmatch = 0
                questionDBDAta.save()

    fileUploadDatabaseList = AdminDB.objects.filter(status=0).order_by('-receivedDate')
    distinctVendors = AdminDB.objects.values('vendorName').distinct()
    context = {"fileNameList": fileUploadDatabaseList, 'distinctVendors': distinctVendors}
    messages.success(request, "Questionnaire File Successfully Uploaded")
    return render(request, "questionnaireApp/uploadNewQuestionnaire.html", context)


def questionnaireDetails(request, clientId):
    questionnaireSearchResult = elasticSearchObject.search(index="question_naire",
                                                           size=9999,
                                                           body={
                                                               "query": {
                                                                   "match": {
                                                                       "clientId": clientId
                                                                   }
                                                               }
                                                           },
                                                           request_timeout=30)

    questionnaireRequiredData = []  # data to be display in table
    vendorName = questionnaireSearchResult['hits']['hits'][0]['_source']['VendorName']
    scope = questionnaireSearchResult['hits']['hits'][0]['_source']['scope']

    for hit in questionnaireSearchResult['hits']['hits']:
        if hit['_source']['clientId'] == clientId:
            questionnaireRequiredData.append(hit['_source'])  # extracting required data

    docLink = AdminDB.objects.get(clientId=clientId).documentLink
    context = {"vendorName": vendorName, "vendorsData": questionnaireRequiredData, "docLink": docLink,
               "dataFromElasticsearch": True, "clientId": clientId, 'scope': scope}
    return render(request, "questionnaireApp/questionnaireDetails.html", context)