import pandas as pd
def createDF():
    newDF = pd.DataFrame({'students': ['s1', 's2', 's3', 's4'], 'teachers': ['t1', 't2', 't3', 't4'],'college': ['c1','c2','c3','c4'],'Science':['10','20','40','2'],'Math':['50','90','40','70']})
    print(newDF)
    newDF['college'] = ['c1','c2','c3','c4']
    newDF['Science'] = [10,30,40,2]
    newDF['Math'] = [50,90,40,70]
    newDF['Total']=newDF.iloc[:,4:6].sum(axis=1)
    print(newDF)
createDF()