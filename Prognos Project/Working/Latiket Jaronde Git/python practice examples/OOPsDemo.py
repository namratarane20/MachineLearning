
# 1.a program to understand class and object creation
# class Student:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
#
#
#     def show(delf):
#         print(delf.name, "-----", delf.age)
#
#
# s = Student("abc", 19)
# print(s.name, "-----", s.age)



# 2.global and nonlocal variables
# def ScopeTest():
#     def do_local():
#         spam = "local spam"
#
#     def do_nonlocal():
#         nonlocal spam
#         spam = "nonlocal spam"
#
#     def do_global():
#         global spam
#         spam = "global spam"
#
#     spam = "test spam"
#     do_local()
#     print("After local assignment:", spam)
#     do_nonlocal()
#     print("After nonlocal assignment:", spam)
#     do_global()
#     print("After global assignment:", spam)
#
# ScopeTest()
# print("In global scope:", spam)

# x = "lebron james"
# def change():
#     x = "jon"
#     print(x)
#     x += " dwaayne wade"
#     print(id(x), x)
#
#
#     def chnage2():
#         nonlocal x
#         x += " plays basektball"
#         print(x)
#
#
#     chnage2()
#     print(x)
#
#
# change()
# print(id(x), x)


# 3.defying a variable of a class from outside of the class using reference variable
# class Complex:
#      def __init__(self, realpart, imagpart):
#          self.r = realpart
#          self.i = imagpart
#
#
# x = Complex(3.0, -4.5)
# print(x.i, x.r)
#
# x.counter = 1
# while x.counter < 10:
#     x.counter = x.counter * 2
# print(x.counter)
# del x.counter  # deletes the counter variable


# inheritance example
# class BaseClass:
#     x = "base string"
#
#     def __init__(self,name):
#         self.name = name
#
#     def call(self):
#         print(self.x, " called within call method")
#
#
# class DerivedClass(BaseClass):
#     def p(self):
#         self.call()
#         print(self.name)
#
#
# DerivedClass("abc").p()


# 4. Data encapsulation example
# class Person:
#     def __init__(self):
#         self.name = 'Manjula'
#         self.__lastname = 'Dube'
#
#     def printName(self):
#         return self.name + ' ' + self.__lastname
#
#
# # Outside class
# P = Person()
# print(P.name)
# print(P.printName())
# print(P.__lastname) # if uncomment it, it'll throw an error for accessing private variable


# 5. abstraction
# class Polygon:
#
#     # abstract method
#     def noofsides(self):
#         pass
#
#
# class Triangle(Polygon):
#
#     # overriding abstract method
#     def noofsides(self):
#         print("I have 3 sides")
#
#
# class Pentagon(Polygon):
#
#     # overriding abstract method
#     def noofsides(self):
#         print("I have 5 sides")
#
#
# class Hexagon(Polygon):
#
#     # overriding abstract method
#     def noofsides(self):
#         print("I have 6 sides")
#
#
# class Quadrilateral(Polygon):
#
#     # overriding abstract method
#     def noofsides(self):
#         print("I have 4 sides")
#
#     # Driver code
#
#
# R = Triangle()
# R.noofsides()
#
# K = Quadrilateral()
# K.noofsides()
#
# R = Pentagon()
# R.noofsides()
#
# K = Hexagon()
# K.noofsides()


# 6. polymorphism
# class Bird:
#     def intro(self):
#         print("There are many types of birds.")
#
#     def flight(self):
#         print("Most of the birds can fly but some cannot.")
#
#
# class sparrow(Bird):
#     def flight(self):
#         print("Sparrows can fly.")
#
#
# class ostrich(Bird):
#     def flight(self):
#         print("Ostriches cannot fly.")
#
#
# b = Bird()
# b.intro()
# b.flight()
#
# s = sparrow()
# s.flight()
# s.intro()
#
# o = ostrich()
# o.flight()


# super keyword example
class Base:
    def __init__(self, name):
        print("inside base class")
        self.name = name

    def show(self):
        print("inside base show method")
        print(self.name)


class Derived(Base):
    def __init__(self):
        print("inside derived class")
        super().__init__("abc")

    def show(self):
        print("inside derived show method")
        super().show()


Derived().show()