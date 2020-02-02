# program to print fibonocci series
def checkFibb():
    n1=0
    n2=1
    c =0
    print(n1,'is fibonacci')
    print (n2,'is fibonacci')
    num = 8
    while c < num+1:
        print(n1)
        nth = n1 + n2

        n1 = n2
        n2 = nth
        c += 1
        
checkFibb()