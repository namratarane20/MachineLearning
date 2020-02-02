# program to swap first and last element of list
def swap():
    l =[1,2,3,4,5,6]
    print ('initial lis is ',l)
    temp = l[0]
    l[0] = l[-1]
    l[-1]=temp
    print('after swaped list is ',l)
swap()

# program to swap any two element in list
def swapTwoPosition():
    l= [1,2,3,4,5,6]

    print ('llist before swapped element',l)
    revList =l.reverse()
    print ('it the reversed list of list', revList)
    
    pos1 = int(input('enter first number '))
    pos2 = int(input('enter the second number '))
    indexOfPos1 = l.index(pos1)
    indexOfPos2 = l.index(pos2)
    temp = l[indexOfPos1]
    l[indexOfPos1]=l[indexOfPos2]
    l[indexOfPos2]= temp
    print('list after swapped element ',l)




    # clear function for clear the all list
    l.clear()
    print('list after  cleard ',l)

swapTwoPosition()

    