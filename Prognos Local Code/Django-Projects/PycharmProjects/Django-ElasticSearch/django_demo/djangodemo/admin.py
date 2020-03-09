from django.contrib import admin
from djangodemo.models import EmpData
#
#
# admin.site.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['ename','eemail']
admin.site.register(EmpData,EmployeeAdmin)