# program to find the given string is palindrom or not
def checkPalindrom():
    string = input('enter the string')
    newString = string[::-1]
    if newString == string:
        print('the string is palindrom')
    else:
        print('the string is not palindrom string')
checkPalindrom()