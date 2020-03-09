from django.db import models

class EmpolyeeDetails(models.Model):
    # eid  = models.IntegerField(max_length=1000)
    ename = models.CharField(max_length=20)
    eemail = models.CharField(max_length=20)
