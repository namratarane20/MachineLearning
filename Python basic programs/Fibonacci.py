# program to print fibonocii series
def fibo():
    num = int(input('enter the number for print Fibonacci series'))
    n1=0
    n2=1
    print(n1)
    print(n2)
    for i in range(2,num):
        term =n1+n2
        n1=n2
        n2=term
        print(term)


fibo()