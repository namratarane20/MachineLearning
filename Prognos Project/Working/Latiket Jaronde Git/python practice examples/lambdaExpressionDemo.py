# lambda expression
# bigger = lambda x, y: x if x>y else y
#
# print(bigger(2,3))


# filter operation
# using normal function
# def even(l):
#     if (l % 2 == 0):
#         return True
#
#
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ans = filter(even, l)
# for x in ans:
#     print(x)

# using lambda function
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ans = list(filter(lambda x: x%2 == 0, l))
# print(ans)


# map()
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ans = map(lambda x: x*x, l)
# print(list(ans))


# reduce()
l = [10,20,30,40,50,60]
from functools import reduce
res = reduce(lambda x,y: x+y, l)
print(res)

