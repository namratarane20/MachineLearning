from django.contrib import admin
from add.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','ename','eemail']

admin.site.register(Employee,EmployeeAdmin)