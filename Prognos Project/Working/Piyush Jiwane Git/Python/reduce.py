from functools import reduce
# lst=[1,2,3,4,5]
# res=reduce(lambda x,y:x+y,lst)
# print("result =",res)

print("enter a serie sof numbers seprated by comma")
lst=[int(x) for x in input().split(",")]
res=reduce(lambda x,y:x if x>y else y,lst)
print("greater value = ",res)
