from elasticsearch import Elasticsearch

elasticSearchObj = Elasticsearch([{'host': 'localhost', 'port': 9200}])
docid = 1


class ElasticSearchOperation:


    def createIndex(self, indexName):
        self.indexName = indexName
        elasticSearchObj.indices.create(index=indexName, ignore=400)

    def checkindex(self, indexName):
        print("does ", indexName, " index exists : ", elasticSearchObj.indices.exists(index=indexName))

    def indexingDocument(self, document):
        global docid
        elasticSearchObj.index(index=self.indexName, doc_type="employee", id=docid, body=document)
        docid = docid + 1

    @staticmethod
    def getindex(indexName, id):
        res = elasticSearchObj.get(index=indexName, doc_type="employee", id=id)
        print("for id ", id, " result ---> ", res)
        print("===============================================================================")
        print("employee id for ", res['_source']['name'], " is ", res['_source']['empid'])

    def searchid(self, indexName, empid):
        result = elasticSearchObj.search(index=indexName, body={
            'query': {
                'match': {
                    'empid':empid
                }
            }
        })
        print(result['hits']['hits'][0]['_source'])


esOp = ElasticSearchOperation()
indexName = str(input("enter index name : "))
esOp.createIndex(indexName)
esOp.checkindex(indexName)

doc1 = {'name':'latiket', 'sirname':'jaronde', 'empid':'TC113', 'team':'engineering'}
doc2 = {'name':'namrata', 'sirname':'rane', 'empid':'TC114', 'team':'engineering'}
doc3 = {'name':'piyush', 'sirname':'jiwane', 'empid':'TC115', 'team':'engineering'}
doc4 = {'name':'nikita', 'sirname':'nanote', 'empid':'TC116', 'team':'engineering'}

esOp.indexingDocument(doc1)
esOp.indexingDocument(doc2)
esOp.indexingDocument(doc3)
esOp.indexingDocument(doc4)

# ElasticSearchOperation.getindex(indexName, 1)
# ElasticSearchOperation.getindex(indexName, 2)
# ElasticSearchOperation.getindex(indexName, 3)
# ElasticSearchOperation.getindex(indexName, 4)

emid = str(input("enter employee id to search : "))
esOp.searchid(indexName, emid)