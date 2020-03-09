# x=lambda n : n * n
#
# print("square of {} = {}".format(2,x(2)))
#
# print("square of {} = {}".format(4,x(4)))

# k=lambda x,y:x+y
#
# print("sum of {} & {} = {}".format(4,4,k(4,4)))
#
# print("sum of {} & {} = {}".format(5,6,k(5,6)))

# k= lambda x,y:x if x>y else y
#
# print("bigger of {} & {} = {}".format(5,4,k(5,4)))
#
# print("bigger of {} & {} = {}".format(2,4,k(2,4)))

def disp(x):
    print("list of values...")
    print("-------------------")
    for i in x:
        print(i)
    print("-------------------")

#main porgram
print("Enter list of values sep by space in same line ")
list1=[int(x) for x in input().split(",")]
disp(list1)