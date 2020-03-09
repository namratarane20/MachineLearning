# class Student:
#     crs="Python"
#     def getValues(self,stno,name,clgname):
#         self.stno=stno
#         self.name=name
#         self.clgname=clgname
#
#     def dispvalues(self):
#         print("student name ",self.name)
#         print("student no ", self.stno)
#         print("student clgname ", self.clgname)
#         print("student course ", Student.crs)
#
# so=Student()
# so.getValues("Ct14024","Piyush Jiwane","KITS Ramtek")
# so.dispvalues()

class Circle:
    PI=3.14
    def set(self):
        self.r=float(input("Enter a radious "))

    def area(self):
        ar=Circle.PI * self.r * self.r
        print("area of circle ",ar)

    def repeat(self):
        self.set()

c=Circle()
c.set()
c.area()
c.repeat()
c.area()
