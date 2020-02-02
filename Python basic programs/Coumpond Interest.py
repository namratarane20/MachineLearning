# program to calculate coumpound interest
def CI():
    p = int(input('enter principle ammount'))
    r = int(input('enter rate'))
    t = int(input('enter time '))
    ci = p * (pow((1+r/100),t))
    print ('the compound interest is ===',ci)
CI()