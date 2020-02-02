# program to culculate sum od square and sum of cubes till entered number
def sumOfAllSq():
    num = int(input('enter the number'))
    sqSum =0
    cubeSum = 0
    for i in range(1,num+1):
        sq = i*i
        cube =i*i*i
        sqSum =sqSum+sq
        cubeSum = cubeSum+cube
    print('sum of square of n natural number is',sqSum)
    print('sum of cube  of n natural number is',cubeSum)


sumOfAllSq()