# def square(x):
#     return x*x
# lst=[1,2,3,4]
# nlst=list(map(square,lst))
#
# print("original list ",lst)
# print("new list ",nlst)

tpl=(10,20,30,40)
ntpl=tuple(map(lambda x:x+2,tpl))

print("original list ",tpl)
print("new list ",ntpl)