class FileDemo:
    def readData(self):
        f=open('D:\\Namrata\\Python-Projects\\python-basics\\python-demo.txt','r')

        content=f.read()
        print(content)
        # content2 will print first line of text file data
        content2=f.readline()
        print(content2)
        # content3 will print ssecond line of text file data
        content3= f.readline()
        print(content3)
myObj=FileDemo()
myObj.readData()