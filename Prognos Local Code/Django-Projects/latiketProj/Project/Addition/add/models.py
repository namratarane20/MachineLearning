from django.db import models
from django.db import models

# Create your models here.
class Employee(models.Model):
    ename = models.CharField(max_length=20)
    eemail = models.CharField(max_length=40)