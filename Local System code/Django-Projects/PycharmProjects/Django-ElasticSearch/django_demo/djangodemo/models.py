from django.db import models



class EmpData(models.Model):
    ename = models.CharField(max_length=30)
    eemail = models.CharField(max_length=30)
# class EmployeeData(models.Model):
#     # eid  = models.IntegerField(max_length=1000)
#     ename = models.CharField(max_length=20)
#     eemail = models.CharField(max_length=20)
