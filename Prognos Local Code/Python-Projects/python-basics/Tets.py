import math
from random import*

# x=10
# def num():
#     print("valu of x==",x)
# num()
#
# print(math.sqrt(16))
# for i in range(10):
#     print(randint(0,9),randint(0,8),randint(0,7),randint(0,6),
#       randint(0,5),randint(0,4),randint(0,3),randint(0,2),randint(0,1))
#
# def data():
#     print("hello")
# data()
# def data1():
#     a=30
#     b=20
#     if(a>b):
#         print("grater")
#     else:
#         print("smaller")
# data1()
def readadata():
    f= open('python-demo2.txt','r+')

    # f.write('namrata \n')
    # f.write('ashok rane from pune \n')
    # f.write(' working at impelsys \n')
    # print('data wri tten to fileS succesfully\n')
    content1=f.readline()
    print(content1,end='')
    content2 = f.readline()
    print(content2,end='')
    content3 = f.readline()
    print(content3)
    # for i in contents:
    #     print(i)
    # print('Name of file is======',f.name)
    # print('mode of file is =====', f.mode)
    # print('file is closed now===', f.closed)
    # print('this file is redable or not===== ', f.readable())
    # print('this file is writable or not ====', f.writable())
    f.close()
    print('file closed',f.closed)
readadata()



# D:\Namrata\Python-Projects\python-basics


