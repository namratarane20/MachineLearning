from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import TagWithInfo, Search,RelevantData

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
    # Fetch keyword to be search
    inSearchKeyword = "Questionnaire Policies"

    if request.POST and recentSearch == None:
        str = request.POST['keyword']
    else:
        str = recentSearch
    # @@Piyush Jiwnae@@ code to count most searched keyword and recently searched keyword
    addToTags(request,str)

    # @@Piyush Jiwnae@@

    print("=============================>", str)
    if ":-" in str:
        getSearchedKeyword = ((str.split(':-', 1)[0]).replace("In@","")).strip()
        if getSearchedKeyword in inSearchKeyword:
            keyword = (str.split(':-', 1)[1]).strip()
            print("---->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", keyword)
            print("with keyword")
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
        if userKeyword.lower() in data['MostRelevantResponses']:
            sortedResponses = [data] + sortedResponses
            print('sorted data ----------->>', sortedResponses)

        else:
            sortedResponses1 = sortedResponses1 + [data]

    # this global Data to be user in relevantResponses method
    # globalRequiredData = sortedResponses
    globalRequiredData = sortedResponses + sortedResponses1

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

    index = 0
    for hit in policiesResultList['hits']['hits']:
        if keyword.lower() in hit['_source']['Data'].lower():
            policiesSearchResult.append(hit['_source'])
            data = policiesSearchResult[index]['Data']
            nextLineCharIndex = len(data) - (data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
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

    # this global policy Data to be user in relevantResponses method
    globalPolicyResult = policiesSearchResult

    tagNameList = []
    allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
    for tags in allTagNameColoumn:
        tagNameList.append(tags.tagName)
        tagNameList = list(dict.fromkeys(tagNameList))

    if getSearchedKeyword.casefold() == 'questionnaire':
        context = {'questionnaireResult': globalRequiredData, 'questionnaireId': questionnaireRequiredId,
                   "tagNameList": tagNameList, 'keyword': keyword, 'active': 'active',
                   'userKeyword': userKeyword.lower()}
    elif getSearchedKeyword.casefold() == 'policies':
        context = {'policiesResult': policiesSearchResult, 'questionnaireId': questionnaireRequiredId,
                   "tagNameList": tagNameList, 'keyword': keyword, 'active': 'active',
                   'userKeyword': userKeyword.lower()}
    elif relevantSearch == 'mostRelevant':
        context = {'questionnaireResult': sortedResponses, 'keyword': keyword, 'userKeyword': userKeyword.lower()}
    else:
        context = {'questionnaireResult': globalRequiredData, 'policiesResult': policiesSearchResult,
                   'questionnaireId': questionnaireRequiredId, "tagNameList": tagNameList, 'keyword': keyword,
                   'active': 'active', 'userKeyword': userKeyword.lower()}

    return render(request, 'questionnaireApp/home.html', context)


def addToTags(request,str=None):
    global globalRequiredData
    key_count = 0

    searchTable = Search.objects.all()
    if str:
        if ":-" in str:
            getSearchedKeyword = ((str.split(':-', 1)[0]).replace("In@", "")).strip()
            print("----------->>>>>",getSearchedKeyword)
            getKeyword = (str.split(':-',1)[1]).strip()
            print("=============================>", getSearchedKeyword)
            print("=============================>",getKeyword)
            newStr = "In@"+getSearchedKeyword+" :- "+getKeyword.casefold()
            print("==============================>",newStr)
            for s in searchTable:
                if (s.keyword == newStr):
                    key_count = 1
                    s.count = s.count + 1
                    s.save()
            if (key_count == 0):
                st = Search()
                st.keyword = newStr
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
    keywordList = []
    retriveData = RelevantData.objects.all().values()
    dataBaseList = list(retriveData)
    print(dataBaseList)
    for i in dataBaseList:
        if i['count'] != 0:
            keywordList.append(i['keywordColumn'])
    globalKeywordList = keywordList
    print("after login ", globalKeywordList)

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

            userName = request.user.get_full_name()

            questionnaireObj = TagWithInfo(vendorname=col1, sectionname=col2, controlname=col3,
                                           securityquestion=col4, response=col5, additionalcomment=col6,
                                           tagName=tagNameWithOutSpaces, tagDescription=tagDesc, userName=userName)

            questionnaireObj.save()

        # logic to pass tagname list

        tagNameList = []
        allTagNameColoumn = TagWithInfo.objects.filter(flag=1)
        for tags in allTagNameColoumn:
            tagNameList.append(tags.tagName)
            tagNameList = list(dict.fromkeys(tagNameList))

        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList':globalKeywordList}
        return render(request, 'questionnaireApp/index.html', context)
    except:
        context = {'tagNameList': tagNameList, 'newSearchTable': newSearchTable, 'order': order,'globalKeywordList':globalKeywordList}
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
    userFirstName = request.user.first_name
    userLastName = request.user.last_name
    user = userFirstName + " " + userLastName

    sortedResponses = []
    sortedResponses1 = []
    keywordList = []

    userKeyword = user + ' ' + globalKeyword

    relevantDataFromDb = RelevantData.objects.all()
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
                if globalKeyword == data.keywordColumn:
                    flag = True
                    data.count += 1
                    data.save()
                    print("keywoord when [] : ", data.keywordColumn, "\n count : ", data.count)
                    break
            if not flag:
                relevantDataFromDb = RelevantData(keywordColumn=globalKeyword, count=1)
                relevantDataFromDb.save()
                print("keywoord : ", relevantDataFromDb.keywordColumn, "\n count : ", relevantDataFromDb.count)

        else:
            if relaventData['MostRelevantResponses'] == []:  # check empty list
                relaventData['MostRelevantResponses'] = [userKeyword.lower()]
                elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                          body=relaventData)
                for data in relevantDataFromDb:
                    if globalKeyword == data.keywordColumn:
                        flag = True
                        data.count += 1
                        data.save()
                        print("keywoord when [] : ", data.keywordColumn, "\n count : ", data.count)
                        break
                if not flag:
                    relevantDataFromDb = RelevantData(keywordColumn=globalKeyword, count=1)
                    relevantDataFromDb.save()
                    print("keywoord : ", relevantDataFromDb.keywordColumn, "\n count : ", relevantDataFromDb.count)

            else:
                if userKeyword.lower() in relaventData['MostRelevantResponses']:
                    relaventData['MostRelevantResponses'].remove(userKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if globalKeyword == data.keywordColumn:
                            flag = True
                            data.count -= 1
                            data.save()
                            print("keywoord when repeted: ", data.keywordColumn, "\n count : ", data.count)
                            break
                    if not flag:
                        relevantDataFromDb = RelevantData(keywordColumn=globalKeyword, count=1)
                        relevantDataFromDb.save()
                        print("keywoord : ", relevantDataFromDb.keywordColumn, "\n count : ", relevantDataFromDb.count)


                else:
                    relaventData['MostRelevantResponses'].append(userKeyword.lower())
                    elasticSearchObject.index(index='question_naire', doc_type='document', id=relaventId,
                                              body=relaventData)
                    for data in relevantDataFromDb:
                        if globalKeyword == data.keywordColumn:
                            flag = True
                            if data.count >= 0:
                                data.count += 1
                            else:
                                data.count=0
                            data.save()
                            print("keywoord when new : ", data.keywordColumn, "\n count : ", data.count)
                            break

                    if not flag:
                        relevantDataFromDb = RelevantData(keywordColumn=globalKeyword, count=1)
                        relevantDataFromDb.save()
                        print("keywoord : ", relevantDataFromDb.keywordColumn, "\n count : ", relevantDataFromDb.count)

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
               'userKeyword': userKeyword.lower()}

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


def displayTagInformation(request, tagname):
    databaseTags = TagWithInfo.objects.filter(tagName=tagname).values()
    addedTagdata = list(databaseTags)
    flagTags = []
    for tag in addedTagdata:
        if tag['flag'] == 1:
            flagTags.append(tag)

    tagDesc = []
    for tagDescription in flagTags:
        # print(tagDescription)
        # print(type(tagDescription))
        # tagDesc.append(tagDescription.get("tagDescription"))
        tagDesc = tagDescription.get("tagDescription")

    return render(request, "questionnaireApp/TagTable.html",
                  {'addedTagdata': flagTags, 'selectedTagName': tagname, 'tagDesc': tagDesc})


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
