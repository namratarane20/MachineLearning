# conditional if statement
# val=int(input("Enter a value "))
# if(val > 5):
#     print("Value greater than 5")
# elif(val < 5):
#     print("Value less than 5")
# else:
#     print("Value equal to 5")
#
# print("out from if-else statement")

# looping while statement
# val=int(input("Enter a value "))
# i=1
# while(i <= val):
#     print("final value = ",i)
#     i +=1
# else: print("final i value = ", i)
# print("out from while statement")

# Looping for loop
# al=int(input("Enter a value "))
# for val in range(1,al+1,2):
#     print(val)

# break statement
# s="PYTHON"
# for ch in s:
#     if(ch == 'H'):
#         break;
#     else:
#         print(ch)
#
# print("over")

#continue statement
# s="PYTHON"
# for ch in s:
#     if(ch == 'H'):
#         print(ch)
#         continue
#     else:
#         print(ch)
#
# print("over")

# Addition program
n=int(input("Enter a number "))
lst=[]
for v in range(1,n+1):
    print(v)
    lst.append(v)

s=0
for sm in lst:
    s=s+sm

print("Sum = ",s)