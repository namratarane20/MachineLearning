# program to check given number is armstrong ot not
def armstrong():
    num = int(input('ennter the number to check whether it is armstrong or not'))
    temp = num
    sum =0
    while temp >0:
        rem = temp%10
        sum = sum+(rem*rem*rem)
        temp =temp//10
    if(sum == num):
        print('this is armstrong number ')

    else:
        print ('this is not armstrong number')

armstrong()