from django.http import HttpResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch

from .models import Employee
# Create your views here.


def home(request):
    return render(request, 'add/home.html')


def sum(request):
    emailData = request.POST['num1']
    emp=Employee.objects.all()
    for e in emp:
        if(e.eemail == emailData):
            # responce = render(request, 'add/result.html')
            success = False
            return render(request, 'add/result.html', {'success': success})

        else:
            # responce = render(request, 'add/home.html')
            success = True
            return render(request, 'add/home.html', {'success':success})


def search(request):
    searchKeyword=request.POST['search']
    from elasticsearch import Elasticsearch
    elasticSearchObject = Elasticsearch("https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
    searchResult = elasticSearchObject.search(index='questionnaire',
                                              size=999,
                                              body={
                                                  "query": {
                                                      "match": {
                                                          "SecurityQuestions": searchKeyword
                                                      }
                                                  }
                                              })

    # return render(request,'add/result.html',{'res':searchResult['hits']['hits']})
    lst=[]
    vendorNameSet = set({})

    for hit in searchResult['hits']['hits']:
        lst.append(hit['_source'])  # extracting required data
        vendorNameSet.add(hit['_source']['VendorName'])

    print(type(vendorNameSet))
    print(vendorNameSet)
    return render(request, 'add/result.html', {'res': lst, 'nameSet': vendorNameSet})


def uploadfile(request):
    uploadOption = True
    success = True
    return render(request, "add/result.html", {'uploadOption': uploadOption, 'success': success})


def indexfile(request):
    from elasticsearch import Elasticsearch
    import csv
    elasticSearchObject = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")

    elasticSearchObject.indices.create(index='questionnaire', ignore=400)  # creating index, ignore if already exists

    for csvFile in request.FILES.getlist('csvfile'):
        from io import TextIOWrapper  # to convert bytes in string
        file = TextIOWrapper(csvFile.file, encoding=request.encoding)  # to get text file
        reader = csv.DictReader(file)  # reading csv

        counter = 1
        for row in reader:
            elasticSearchObject.index(index='questionnaire', doc_type='document', id=str(csvFile) + str(counter), body=row)  # indexing file
            counter += 1

        try:
            while True:
                elasticSearchObject.delete(index='questionnaire', doc_type='document', id=str(csvFile)+str(counter))
                counter += 1
        except:
            pass

    uploadOption = True
    success = True
    return render(request, 'add/result.html', {'uploadOption': uploadOption, 'success': success})


def toSearchPage(request):
    return render(request, 'add/result.html')
