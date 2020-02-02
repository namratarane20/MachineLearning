# count the number oocuurance of element in list
def count():
    l=[1,2,3,4,5,6,3,4,25,11]
    count =0
    ele = input('enter the element to  check occurence')
    for i in l:
        if(i == ele):
            count +=1
    print ('occurence of ',ele ,'is ',count,'times' )


    # code to find aathe additon of element in list
    sum =0
    for i in l:
        sum = sum +i
    print('addition of all element in list',sum)
    print(min(l))
    print(max(l))
    # code to find second largest number in list
    l.remove(max(l))
    print('second largest number form list',max(l))


count()
