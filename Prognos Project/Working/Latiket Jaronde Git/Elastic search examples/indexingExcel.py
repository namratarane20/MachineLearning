from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


class ElasticSearchOperation:

    def indexingToElasticSearch(self, path):

        # try:
        #     es.indices.delete(index='questions')
        # except:
        #     pass
        #
        es.indices.create(index='questions1', ignore=400)

        with open(path) as f:
            reader = csv.DictReader(f)
            helpers.bulk(es, reader, index='questions', doc_type='my-type')


        # with open(path) as f:
        #     data = f.read()
        #     print(data)

    def searchKeyword(self, keyword):
        # searchResult = es.search(index="questions", body={
        #     'query': {
        #         'match': {
        #             'Security Questions:': keyword
        #         }
        #     }
        # }, size=1000)

        searchResult = es.search(index='questions', body= {
            'query': {
                'bool': {
                    'must': [{
                        'match': {
                            'term': {
                                'Vendor Name': 'Highmark Health '
                            }
                        },
                        'match': {
                            'Security Questions:': keyword
                        }
                    }]
                }
            }
        }, size=999)
        outputList = searchResult['hits']['hits']
        print(len(outputList))
        for i in outputList:
            # print((searchResult['hits']['hits'][i]['_source']).values)
            x = i['_source']
            print(x['Vendor Name'], " == ", x['Security Questions:'], " == ", x['Service/Solution Response'], " == ", x['Service/Solution Comments'])


esop = ElasticSearchOperation()
# y = True
# while y:
#     path = str(input("enter path of string : "))
#     # inpath = "r'"+path+"'"
#     esop.indexingToElasticSearch(path)
#     ip = str(input("do you want to import another file : "))
#     if ip=='yes' or ip=='Yes':
#         y = False

# path = "C:\Users\latiket.jaronde\Downloads"
# esop.indexingToElasticSearch(r"C:\Users\latiket.jaronde\Downloads\cantUpload\CORL_updated.csv")

print("======================================================================================")
keyword = str(input("enter a keyword to search : "))
esop.searchKeyword(keyword)
