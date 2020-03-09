from elasticsearch import Elasticsearch, helpers
import csv


elasticSearchObject = Elasticsearch(
    'https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443')


class ElasticSearchOperations:

    @staticmethod
    def createIndex():
        global elasticSearchObject
        elasticSearchObject.indices.create(index='questionnaire', ignore=400)

    @staticmethod
    def indexDocument(path):
        global elasticSearchObject

        with open(path) as f:
            reader = csv.DictReader(f)
            helpers.bulk(elasticSearchObject, reader, index="questionnaire", doc_type='my-type')

    @staticmethod
    def searchKeyword(keyword):
        global elasticSearchObject
        searchResult = elasticSearchObject.search(index='questionnaire',
                                                  size=999,
                                                  body={
                                                      "query": {
                                                          "match": {
                                                              "SecurityQuestions": keyword
                                                          }
                                                      }
                                                  })
        for hit in searchResult['hits']['hits']:
            print(hit['_source'])


elasticSearchOperationObject = ElasticSearchOperations()
# while y == 1:
#     choice = int(input("choose operation: \n1. Indexing a document\n2. Searching for a particular keyword "))
#     if choice == 1:
#         # path = str(input("enter input path: "))
#         path = r""
#         elasticSearchOperationObject.indexDocument(path)
#     elif choice == 2:
#         keyword = str(input("enter a keyword to search in Security Questions: "))
#         elasticSearchOperationObject.searchKeyword(keyword)
#
#     y = int(input("to continue, enter 1 : "))

elasticSearchOperationObject.createIndex()
# elasticSearchOperationObject.indexDocument(r"C:\Users\latiket.jaronde\Downloads\cantUpload\Aetna.csv")
res = elasticSearchObject.search(index='questionnaire', size=9999, body={})
print(len(res['hits']['hits']))

