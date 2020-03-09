class Parent:
    parrentVar =100

    def __init__(self): # syntax for constructor
        print("calling parent constructor")

    def parentMethod(self):
        print('calling parent method')

    def setAttr(self,attr):
        Parent.parrentVar = attr

    def getAttr(self):
        print("parent attribute is : ",Parent.parrentVar)

class Child(Parent) :
    def __init__(self):
        print('calling child constructor')
    def childMethod(self):
        print('calling child method')


c= Child()
c.childMethod()
c.parentMethod()
c.setAttr(500)
c.getAttr()
Parent()
Parent()