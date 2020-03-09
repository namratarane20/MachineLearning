from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch('https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443')

es.indices.create(index="demo", ignore=400)

print(es.indices.exists(index="demo"))

# doc = {
#     "name": "akg",
#     "sir name": "jhu",
#     "age": 14
# }

# es.index(index="demo", body=doc)

# with open(r"C:\Users\latiket.jaronde\Downloads\cantUpload\BioReference.csv") as f:
#     reader = csv.DictReader(f)
#     helpers.bulk(es, reader, index="demo", doc_type='my-type')

res = es.search(index="demo", body={
    "query": {
        "match": {
            "Security Questions:": "security"
        }
    }
}, size=999)

print(res['hits']['hits'][0]['_source']["Security Questions:"])
