def f():
    localVar= "this is local variable"
    print(localVar)


# Global scope
f()
globalVar='this is global variable'
print(globalVar)
# f()
def f2():
    global s
    print(s)
    s=' this is global variable with global keyword'
    print(s)
s=' this is'
f2()