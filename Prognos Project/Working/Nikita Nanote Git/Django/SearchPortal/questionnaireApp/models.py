from django.db import models

# Create your models here.


class EmployeeDetails(models.Model):
    employeeName = models.CharField(max_length=64)
    employeeEmail = models.CharField(max_length=64)
