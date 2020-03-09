# from django.contrib import admin
# from questionnaireApp.models import EmployeeDetails
# # Register your models here.
#
#
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employeeName']
#
#
# admin.site.register(EmployeeDetails)
from django.contrib import admin
from questionnaireApp.models import TagsInformation
class QuestionnaireAdmin(admin.ModelAdmin):

     admin.site.register(TagsInformation)