# program to find enterd string is anagaram or not
def anagram():
    s1=input('Enter fisrt string====')
    s2=input('Enter second string======')
    sortedS1 = sorted(s1)
    sortedS2 = sorted(s2)
    if sortedS1 == sortedS2:
        print ('the Strings are anagram======')
    else:
        print ('THer strings are not anagram======')
anagram()

