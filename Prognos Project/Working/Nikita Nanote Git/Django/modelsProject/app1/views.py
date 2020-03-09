from django.shortcuts import render
from app1.models import Employee
def employee_info_view(request):
    employees=Employee.objects.all()
    return render(request,'app1/result.html',{'employees':employees})
