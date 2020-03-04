from django.contrib import admin
from ssoapp.models import Profile
class Profile(admin.ModelAdmin):

  admin.site.register(Profile)
#
# class Employee(admin.ModelAdmin):
#     list_display = ['id']
#
#
# admin.site.register(Profile,Employee)