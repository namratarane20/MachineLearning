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
from questionnaireApp.models import TagWithInfo,Search
class QuestionnaireAdmin(admin.ModelAdmin):
     admin.site.register(TagWithInfo)

admin.site.register(Search)