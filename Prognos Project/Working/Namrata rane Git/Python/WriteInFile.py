def readData():
    f= open('python-demo.txt','r')
    content1=f.read()
    print(content1)
    f.close()
readData()


def writeData():
    f2= open('python-demo3.txt','w')
    f2.write("hello  data written here in this file")
    print('data written to file succesfully')

    f2=open('python-demo3.txt','r')
    writtenContent = f2.read()
    print(writtenContent)
writeData()

def appendData():
    f3= open('python-demo.txt','a')
    f3.write('this is appended data /n')
    # f3.close()

    f4= open('python-demo.txt','r')
    redContent = f4.read()
    print(redContent)
appendData()

