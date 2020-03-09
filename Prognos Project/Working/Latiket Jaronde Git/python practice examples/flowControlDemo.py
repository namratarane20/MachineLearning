# if-elif-else loop demo
# biggest of three numbers
# num1 = int(input("first number"))
# num2 = int(input("second number"))
# num3 = int(input("third number"))
#
# if num1 > num2:
#     if num1 > num3:
#         print(num1, " is biggest")
#     else:
#         print(num3, " is biggest")
# else:
#     if num2 > num3:
#         print(num2, " is biggest")
#     else:
#         print(num3, " is biggest")


# while loop
# generating number table
# num = int(input("enter number : "))
# i = 1
# while i <= 10:
#     print(num, "*", i, " = ", num*i)
#     i += 1

# for loop
# generating number table
# num = int(input("enter number : "))
# for i in range(1, 11):
#     print(num, "*", i, " = ", num * i)

# break statement
# string = "python"
# for s in string:
#     if s == 'h':
#         break
#     else:
#         print(s)

# continue statement
for i in range(10):
    print("statement before continue")
    continue
    print("statement after continue")
else:
    print("end of for")

