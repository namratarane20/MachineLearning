# program to print the factorial of number
def fact():
    fact = 1
    num = int(input('Enter the number for factorial'))
    for i in range(1,num+1):
       fact = fact* i
    print('factorial is===',fact)
fact()






















