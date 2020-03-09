# A fuction taking value and returning value
# def add(x,y):
#     return a+b
# #main function
# a=int(input("Enter first number "))
# b=int(input("Enter second number "))
# print("Sum = ",add(a,b))

# A function NOT taking value and NOT returning value
# def add():
#     a = int(input("Enter first number "))
#     b = int(input("Enter second number "))
#     print("Sum = ",a+b)
# #main function
#
# add()
# add()

#returning multiple values
# def sop(x,y):
#     c=x+y
#     d=x-y
#     e=x*y
#     f=x/y
#     return (c,d,e,f)
# # main program
# x=int(input("Enter first number "))
# y=int(input("Enter second number "))
# z=sop(x,y)
# print("Sum = ",z[0])
# print("Sub = ",z[1])
# print("Mul = ",z[2])
# print("Div = ",z[3])

# def details(no,name,mark):
#     print("Roll number = ",no)
#     print ("Name = ",name)
#     print ("Marks = ",mark)
#
# details("CT14024","Piyush Jiwnae",56.65)
# print ("-----------------------")
# details(name="Piyush Jiwnae", mark=76.56, no="CT14024")

# def display(*a):
#     for x in a:
#         print(x)

#main program
# display(10)
# print("-------------------")
# display(10,20)
# print("-------------------")
# display("Piyush","jiwane",20,499887597587.4765743685)
# print("-------------------")

# def showInfo(**x):
#     print("record information")
#     print("-------------------")
#     for (k,v) in x.items():
#         print(k,"----",v)
#
# # main program
# showInfo(sname="Piyush",cpp=60,c=70,python=90)
# print("-------------------")
# showInfo(fname="Piyush",subj1="sj",sub2="math",sub1="sdjs")

a=10
b=20
c=30
d=40
def operation():
    global c,d
    c=c+1
    d=d+1
    a=100
    b=200
    x=globals()['a']
    y=globals()['b']
    res=a+b+x+y+c+d
    print("result = ",res)

operation()
print(a,b,c,d)