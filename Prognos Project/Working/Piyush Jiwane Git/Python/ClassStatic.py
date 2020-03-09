class Increment:
    count = 0
    def __init__(self):
        Increment.count = Increment.count+1

    @classmethod
    def callMethod(cls):
        print("No of object created ",cls.count)

    
    def sum(x,y):
        return x+y

inc1=Increment()
inc2=Increment()

inc2.callMethod()
print("Sum =",inc1.sum(10,20))

print("final sum =",Increment.sum(1,2))
