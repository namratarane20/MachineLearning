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
    createdBy = models.CharField(max_length=100)
    updatedBy = models.CharField(max_length=100)
    destroyedBY = models.CharField(max_length=100)


class Search(models.Model):
    keyword = models.CharField(max_length=30)
    count = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword+" "+str(self.count)


class RelevantResponseDatabase(models.Model):
    userKeyword = models.CharField(max_length=60)
    count = models.IntegerField()
    keywordSearched = models.CharField(max_length=30)


class UserSessionDatabase(models.Model):
    userName = models.CharField(max_length=100)
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName


class KeywordSearchedDatabase(models.Model):
    userName = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName + " " + self.keyword


class MostFavouredResponseHistoryDatabase(models.Model):
    userName = models.CharField(max_length=100)
    vendorName = models.CharField(max_length=100)
    question = models.TextField()
    response = models.TextField()
    additionalComment = models.TextField()
    status = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.userName + " " + self.status


class FileUploadReport(models.Model):
    fileName = models.CharField(max_length=200)
    noOfRows = models.IntegerField()
    uploadedBy = models.CharField(max_length=100)
    updatedBy = models.CharField(max_length=100)
    uploadedTime = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName + " " + self.fileName

class AdminDB(models.Model):
    vendorName = models.CharField(max_length=100)
    summery = models.CharField(max_length=500)
    recivedDate = models.DateTimeField()
    spradsheetLink = models.CharField(max_length=100)
    relativeCommunication = models.CharField(max_length=500)
    fileName = models.CharField(max_length=100)
    clientId = models.CharField(max_length=100)

class QuestionDB(models.Model):
    vendorName = models.ForeignKey(AdminDB, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    response = models.CharField(max_length=400)
    additionalComment = models.CharField(max_length=400)
    assignTo = models.CharField(max_length=400)
    assignBy = models.CharField(max_length=400)

