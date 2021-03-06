from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import TagWithInfo, Search,RelevantResponseDatabase
from django.contrib import messages
from .models import Image

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
    return addToTags(request)
    # return render(request, 'questionnaireApp/home.html')


@login_required
@transaction.atomic
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
# End of sign in functinality==========================================================================


# searching keyword in elasticsearch index
def searchKeyword(request, recentSearch=None,relevantSearch=None):
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

        # Fetch user from SSO
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2

    userKeyword = user + ' ' + keyword

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
                        print("upper case data after : ", upperCaseData)
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
        elif getSearchedKeyword.casefold() == 'policies':
            context = {'policiesResult': policiesSearchResult, 'questionnaireId': questionnaireRequiredId,
                       "tagNameList": tagNameList, 'keyword': keyword, 'policyActive': 'active',
                       'userKeyword': userKeyword.lower()}
        elif relevantSearch == 'mostRelevant':
            context = {'questionnaireResult': sortedResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower(),
                       'questionnaireActive': 'active'}

        else:
            context = {'questionnaireResult': globalRequiredData, 'policiesResult': policiesSearchResult,
                       'questionnaireId': questionnaireRequiredId, "tagNameList": tagNameList, 'keyword': keyword,
                       'questionnaireActive': 'active', 'userKeyword': userKeyword.lower()}

        return render(request, 'questionnaireApp/home.html', context)

    else:
        messages.success(request, "Data not available for " + keyword + " keyword.")
        return addToTags(request)

def addToTags(request,str=None):
    print("addd to tags")
    global globalKeyword
    user1 = request.user.first_name
    user2 = request.user.last_name
    user = user1 + " " + user2
    userKeyword = user + ' ' + globalKeyword
    global globalRequiredData
    key_count = 0
    keywordList = []

    imageObject = list(Image.objects.all().values())
    print("objects : ", imageObject)

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

        # print("-------->>------>>",usr.userName)
        # print("------>>-------->>",keywordQuerySet)
        # print("---------->>",uniqueKey)

        imgUsrDict.update({usr.userName:{'alias':imgStr,'colorCode':hex_number,'keyData':uniqueKey}})
        print('---------->>---->>',imgUsrDict)
        # imgUsrDict.update({usr.userName:{imgStr:hex_number}})
        imgStr=""
        uniqueKey = []


    # colorCode = []
    # import random
    #
    # for usrCount in imageObject:
    #     random_number = random.randint(0, 16777215)
    #     hex_number = format(random_number, 'x')
    #     hex_number = '#' + hex_number
    #     colorCode.append(hex_number)

    # print("---------->>-------->>",colorCode)
    #
    #
    print("------------>>------------>>",imgUsrDict)
    #
    #
    # print('--------------->>--------------->>',imgStr)

    searchTable = Search.objects.all()
    if str:
        if ":-" in str:
            getSearchedKeyword = ((str.split(':-', 1)[0]).replace("in@", "")).strip()
            getKeyword = (str.split(':-',1)[1]).casefold().strip()
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
    newSearchTable = nst.order_by('-count')[:10]
    order = nst.order_by('-updated_at')

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
            tagNameWithOutSpaces = tagname.strip()# "strip" ==> to remove left and right side spaces from tagName(which is str)
            tagDesc = request.POST['tagDescription']
            if tagDesc == '':
                tagDescQuerySet = TagWithInfo.objects.filter(tagName=tagNameWithOutSpaces).values()

                tagDescList = list(tagDescQuerySet)
                for tagDescription in tagDescList:
                    tagDesc = tagDescription.get("tagDescription")
            else:
                tagDesc = request.POST['tagDescription']

            updatingTag = False
            creatingTag = False
            if TagWithInfo.objects.filter(tagName=tagname).count() > 0:
                tagsDbObject = TagWithInfo.objects.filter(tagName=tagname).order_by('-dateTime')
                tagCreatedBy = tagsDbObject[0].createdBy
                updatingTag = True
            else:
                creatingTag = True

            # userName = request.user.get_full_name()
            if creatingTag:
                TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3, securityquestion=col4, response=col5,
                            additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                            userName=userName, createdBy=userName).save()
            elif updatingTag:
                TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3, securityquestion=col4, response=col5,
                            additionalcomment=col6, tagName=tagNameWithOutSpaces, tagDescription=tagDesc,
                            userName=userName, createdBy=tagCreatedBy, updatedBy=userName).save()




            # questionnaireObj = TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3,
            #                                securityquestion=col4, response=col5, additionalcomment=col6,
            #                                tagName=tagNameWithOutSpaces, tagDescription=tagDesc, userName=userName)
            #
            # questionnaireObj.save()

        # logic to pass tagname list


        # tagNameList = []
        # allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        # for tags in allTagNameColoumn:
        #     tagNameList.append(tags.tagName)
        #
        #     tagNameList = list(dict.fromkeys(tagNameList))

        tagNameList = []
        tagNameDict = {}
        usrNameSet = set({})
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))
            usrNameSet.add(tags.createdBy)
            usrNameSet.add(tags.updatedBy)

        print("----------------->>",usrNameSet)

        lst=set({})
        for userName in usrNameSet:
            if userName != '':
                for tags in allTagNameColoumn:
                    if userName == tags.createdBy :
                        lst.add(tags.tagName)
                    if userName == tags.updatedBy:
                        lst.add(tags.tagName)

                tagNameDict.update({userName:lst})
                print('--------------------->>',tagNameDict)
                lst=set({})

        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList':globalKeywordList,'ProfileImage':imageObject,'tagNameDict':tagNameDict,'imgUsrDict':imgUsrDict}
        return render(request, 'questionnaireApp/index.html', context)
    except:
        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList':globalKeywordList,'ProfileImage':imageObject,'tagNameDict':tagNameDict,'imgUsrDict':imgUsrDict}
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
            # here we get data which is selected by checkboxes
            relaventData = globalRequiredData[int(id) - 1]
            # here we get id of that selected data
            relaventId = relaventData.get('ID')
            # after work of Id is done of comparision so to get correct records, it is deleted
            # relaventData.pop('ID')
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
                relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1, keywordSearched = globalKeyword)
                relevantDataFromDb.save()

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
                    relevantDataFromDb = RelevantResponseDatabase(userKeyword=userKeyword, count=1, keywordSearched=globalKeyword)
                    relevantDataFromDb.save()

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

    context = {'questionnaireResult': globalRequiredData, 'policiesResult': globalPolicyResult, 'keyword': globalKeyword,
               'userKeyword': userKeyword.lower(), "questionnaireActive": 'active'}

    return render(request, 'questionnaireApp/home.html', context)


def recentSearchKeyword(request, recentSearch):
    if request.GET.get('name') == 'mostRelevant':
        return searchKeyword(request,recentSearch,relevantSearch='mostRelevant')
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

    messages.success(request, "Questionnaire File Successfully Uploaded")
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

    messages.success(request, "Policy File Successfully Uploaded")
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
        messages.success(request, 'Data related to tag '+tagname+' is not available in the Database, please search for the correct Tag Name')
        return addToTags(request)

def destroyTagInformation(request):
    destroyedTagName = request.POST['destroyedTagName']
    destroyTagsData = TagWithInfo.objects.filter(tagName=destroyedTagName).update(flag=0)
    flag0data = TagWithInfo.objects.filter(tagName=destroyedTagName).values()
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
