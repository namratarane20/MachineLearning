class Parent:
    def __init__(self,prop=0):
        self.pprop=prop

    def showProperty(self):
        print("Parent property ",self.pprop)

class Chile1(Parent):
    def __init__(self,prop1=0,prop2=0):
        super().__init__(prop1)
        self.cprop=prop2

    def showProperty(self):
        super().showProperty()
        print("Child property ",self.cprop)
        print("Total property ",(self.cprop + self.pprop))

# main program
c=Chile1(3000,500)
c.showProperty()