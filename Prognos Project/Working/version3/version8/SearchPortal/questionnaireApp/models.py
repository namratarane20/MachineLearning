# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,unique=True, null=False, db_index=True,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Database to store tags information
class TagWithInfo(models.Model):
    vendorname = models.CharField(max_length=1000)
    sectionname= models.CharField(max_length=1000)
    controlname = models.CharField(max_length=1000)
    securityquestion = models.CharField(max_length=1000)
    response = models.CharField(max_length=1000)
    additionalcomment = models.CharField(max_length=1000)
    tagName = models.CharField(max_length=1000)
    tagDescription = models.CharField(max_length=1000)
    flag = models.IntegerField(default=1)
    dateTime = models.DateTimeField(auto_now=True)
    userName = models.CharField(max_length=100)


class Search(models.Model):
    keyword = models.CharField(max_length=30)
    count = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword+" "+str(self.count)

class RelevantResponseDatabase2(models.Model):
    userKeyword = models.CharField(max_length=60)
    count = models.IntegerField()
    keywordSearched = models.CharField(max_length=30)
    userList = models.CharField(max_length=60)