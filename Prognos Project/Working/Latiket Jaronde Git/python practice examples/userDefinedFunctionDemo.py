
# def add(a: int, b: int):
#     return a+b, a-b, a*b, a/b
#
#
# a = int(input("enter first number : "))
# b = int(input("enter second number : "))
# sum, sub, mul, div = add(a, b)
# print("sum = ", sum)
# print("sub = ", sub)
# print("multiple = ", mul)
# print("divide = ", div)


# keyword argument parameter
# def add(a: int, b: float):
#     return a+b
#
#
# print(add(b=3.2, a=2))


# "variable length"
# def show(*data):
#     for x in data:
#         print(x)
#
#
# show(10)
# show(20, 30)


#keyword variable parameter
# def show(**data):
#     for k,v in data.items():
#         print(k, "---", v)
#
#
# show(name="lebron", sport="basketball", age="34")

# operations on global variable
a, b, c = 10, 20, 30
def fun():
    global b # accessing global variable locally
    a = 100 # local variable with same name as global variable
    c = a+b
    print("a = ", a, "b = ", b, "c = ", c)


fun()
print("a = ", a, "b = ", b, "c = ", c)
