# program to find even and odd  number form list
def even():
    myList =[12,23,14,5,18,4,40,10,33]
    eventList = []
    oddList= []
    for i in myList:
        if i % 2 == 0:
            eventList.append(i)
        else:
            oddList.append(i)
    print ('this is even number list',eventList)
    print ('this is odd numbers list',oddList)
even()
# program to find even and odd number form list in specific range
def evenOddInRange():
    l = [20,3,7,4,6,5,7,22,10,50,34,27,28,59,60]
    evenListInrange = []
    oddListInRnage= []
    start = int(input('enter start range'))
    end = int(input('enter end range'))
    for i in l:
        if i <= end and i >= start:
            if i%2 ==0 :
                evenListInrange.append(i)
            else:
                oddListInRnage.append(i)
    print ('this is my even list in range',evenListInrange)
    print ('this is my odd list in range',oddListInRnage)
evenOddInRange()





