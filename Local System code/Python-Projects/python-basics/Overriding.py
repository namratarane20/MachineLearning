class Parent:
    def myMethod(self):
        print('calling parent method ')

class Child(Parent):
    def myMethod(self):
        super().myMethod()
        print("calling child method ")
        return super().myMethod()
c= Child()
c.myMethod()


# calling parent method
# calling child method
# calling parent method

