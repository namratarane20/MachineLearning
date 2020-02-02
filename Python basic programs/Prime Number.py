# program to check number in prime or not
def isPrime():
   num =int(input('Enter the number:-->'))
   if num >1:
       for i in range(2,num):
           if(num % i) == 0:
               print (num,'is not prime number')
               break
       else:
            print (num,'is prime number')
   else:
       print (num,'is not prime number ')
isPrime()



def findPrimeNumbers():
    start =int(input('Enter start number'))
    end = int(input('Enter last'))
    for val in range(start,end+1):
        if val>1:
            for i in range(2,val):
                if(val % i)==0:
                    break
            else:
                print(val)
findPrimeNumbers()

