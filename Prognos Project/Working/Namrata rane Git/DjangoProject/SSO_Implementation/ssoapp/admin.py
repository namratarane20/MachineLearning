from django.contrib import admin
from ssoapp.models import Profile
#
#
# admin.site.register(Employee)

class Employee(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(Profile,Employee)