# def isPos(x):
#     if(x > 0):
#         return True
#     else:
#         return False
#
# def isNeg(x):
#     if(x < 0):
#         return True
#     else:
#         return False
#
# def disp(list):
#     print("=============")
#     for x in list:
#         print(x)
#     print("=============")
#
# # main program
# list1=[1,2,-3,-4,5,-6,-7,8,9]
# fobj1=filter(isPos,list1)
# posList=list(fobj1)
# disp(posList)
# fobj2=filter(isNeg,list1)
# negList=list(fobj2)
# disp(negList)

# print("Enter many values ")
# lst1=[int(x) for x in input().split()]
#
# plist=list(filter(lambda x:x>0,lst1))
# nlist=list(filter(lambda x:x<0,lst1))
#
# print("original list " , lst1)
# print("pos list " , plist)
# print("neg list " , nlist)

def vowel(x):
    v=['a','b','c','d','e']
    if x not in v:
        return True
    else:
        return False

alp=['a','z','d','e','r']
vl=list(filter(vowel,alp))
print("original value ", alp)
print("filterd value ",vl)
