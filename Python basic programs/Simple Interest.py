# program to calculate simple interest
def findInterest():
    p= int(input('Enter principle ammount'))
    r=int(input('Enter rate'))
    t= int(input('Enter time'))
    si= (p*r*t)/100
    print('interest is ',si)
findInterest()