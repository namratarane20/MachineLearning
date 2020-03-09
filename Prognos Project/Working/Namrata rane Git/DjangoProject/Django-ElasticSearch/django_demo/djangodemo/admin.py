from django.contrib import admin
from djangodemo.models import EmpolyeeDetails
#
#
# admin.site.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['ename','eemail']
admin.site.register(EmpolyeeDetails,EmployeeAdmin)