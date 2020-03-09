from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch
import csv
elasticsearchObj = Elasticsearch("https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
#
def fun(request):
    return  render(request,'demoapp/result.html')

def createIndex(request):
    elasticsearchObj.indices.create(index='elasticsearch_index_demo1', ignore=400)
    return render(request, 'demoapp/result.html')

def indexing(request):

