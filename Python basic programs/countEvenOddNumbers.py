# program for count the even and odd numbers in list
def countEvenOdd():
    l =[1,2,3,4,5,6,7,8,9,10,2,2,2,2]
    eveCount =0
    oddCount=0
    for i in l:
        if i%2==0:
            eveCount+=1
        else:
            oddCount+=1
    print ('the count of even numbers in list is==',eveCount)
    print ('the count of odd numbers in list is==',oddCount)
countEvenOdd()