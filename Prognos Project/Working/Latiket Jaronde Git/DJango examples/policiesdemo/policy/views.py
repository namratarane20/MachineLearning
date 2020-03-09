from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'index.html')


def index(request):
    from elasticsearch import Elasticsearch
    es = Elasticsearch("https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
    es.indices.create(index="policies", ignore=400)
    for docFile in request.FILES.getlist('docFile'):
        fileName = str(docFile)[:str(docFile).rfind('.')]
        from docx import Document
        # import docx2txt
        document = Document(docFile)
        # document = docx2txt.process(docFile)
        textList = []
        for paragraph in document.paragraphs:
            textList.append(paragraph.text)
        textData = '\n'.join(textList)
        data = {'PolicyName': fileName, 'Data': textData, 'Link': request.POST['link']}
        # data = {'Data': textData, 'Link': url}
        es.index(index='policies', id=docFile, body=data)

    return render(request, 'index.html')


def search(request):
    from elasticsearch import Elasticsearch
    es = Elasticsearch(
        "https://search-security-questionnarie-7n2rpbfx6hafbye4k4xzfj7z4e.us-east-1.es.amazonaws.com:443")
    keyword = request.POST['keyword']
    resultList = es.search(index='policies',
                           size=9999,
                           body={
                               'query': {
                                   'match': {
                                        'Data': keyword
                                   }
                               }
                           })
    # print("result : ", resultList['hits']['hits'][0]['_source']['PolicyName'])
    policiesSearchResult = []

    for i, hit in enumerate(resultList['hits']['hits']):
        policiesSearchResult.append(hit['_source'])
        data = hit['_source']['Data']
        nextLineCharIndex = len(data) - (data[::-1].find("\n", len(data) - data.lower().find(keyword.lower()) - 1))
        lastIndex = data.find(".", nextLineCharIndex)
        import re
        while True:
            if len(re.findall(r'\w+', data[nextLineCharIndex:lastIndex + 1])) < 40:
                lastIndex = data.find(".", lastIndex+2)
            else:
                break
        policiesSearchResult[i]['Data'] = data[nextLineCharIndex:lastIndex + 1]
        print("policies data: ", policiesSearchResult[i]['Data'])

    return render(request, 'index.html', {'policyresult': policiesSearchResult})
