# program to remove duplicate from list and add it to anathor list
def dupliacateList():
    l = [1,2,3,4,5,6,7,2,3,4,9]
    print(sorted(l))
    dupList = []
    for i in l:
        if i not in dupList:
            dupList.append(i)
    print ('this is the dupliacate element form list',dupList)
dupliacateList()