def printpyramid(num):
    for i in range(0,num):
        for j in range(0,i+1):
            print('* ',end="")
        print("\r")
printpyramid(10)

def loop():
    count=0
    while(count < 5):
        count= count+1
        print('welcome to prognos')
    else:
     print('else blocck here')
loop()


def listLoop():
    list = ['nikita', 'namrata', 'piyush', 'latiket']
    for i in range(len(list)):
        print(list[i])
listLoop()

def dictLoop():
    d = {'name':'namrata','id':'tc114','mail':'@namu'}
    for i in d.keys():
        print('keys from dict type',i)
    for i in d.values():
        print('values from dict type',i)
    for i in d.items():
        print('key and values from dict',i)
dictLoop()