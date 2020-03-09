from django.shortcuts import render
from questionnaireApp.models import EmployeeDetails
# Create your views here.


def userLogin(request):
    return render(request, 'questionnaireApp/userLogin.html')


def mailVerification(request):
    emailData = request.POST['emailId']
    employeeList = EmployeeDetails.objects.all()
    for employee in employeeList:
        if employee.employeeEmail == emailData:
            return render(request, 'questionnaireApp/home.html')

        else:
            validate = True
            return render(request, 'questionnaireApp/userLogin.html', {'validate': validate})


def searchKeyword(request):
    keyword = request.POST['keyword']
    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
    searchResult = elasticSearchObject.search(index='questionnaire',
                                              size=9999,
                                              body={
                                                  "query": {
                                                      "match": {
                                                          "SecurityQuestions": keyword
                                                      }
                                                  }
                                              })

    requiredData = []  # data to be display in table
    vendorNameSet = set({})

    for hit in searchResult['hits']['hits']:
        requiredData.append(hit['_source'])  # extracting required data
        vendorNameSet.add(hit['_source']['VendorName'])

    return render(request, 'questionnaireApp/home.html', {'result': requiredData, 'nameSet': vendorNameSet})


def uploadcsv(request):
    return render(request, 'questionnaireApp/uploadcsv.html')


def toHomePage(request):
    return render(request, 'questionnaireApp/home.html')


def indexToElasticsearch(request):
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

    return render(request, 'questionnaireApp/uploadcsv.html')
