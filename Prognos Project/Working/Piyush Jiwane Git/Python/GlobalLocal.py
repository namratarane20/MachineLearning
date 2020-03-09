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