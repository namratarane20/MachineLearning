# program to copy the perticular list(called as clonning)
def Clonning(l):
    copyList = list(l)
    return copyList
def clone():
    l=[1,2,3,4,5,6]
    print ('fist list',l)
    copyList = Clonning(l)
    print('copy of the list',copyList)
clone()