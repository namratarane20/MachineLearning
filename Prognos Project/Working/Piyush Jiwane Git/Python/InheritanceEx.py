from Student import Student
from Teacher import Teacher

so=Student()
so.setId(101)
so.setName("Piyush Jiwane")
so.setAddr("Hyd")
so.setMark(90.98)


print("Student Id =",so.getId())
print("Student Name =",so.getName())
print("Student Addr =",so.getAddr())
print("Student Mark =",so.getMark())
print("=========================")

tch=Teacher()
tch.setId(10101)
tch.setName("Piyush Jiwane")
tch.setAddr("Hyd")

print("Teacher Id =",tch.getId())
print("Teacher Name =",tch.getName())
print("Teacher Addr =",tch.getAddr())
print("===========================")


