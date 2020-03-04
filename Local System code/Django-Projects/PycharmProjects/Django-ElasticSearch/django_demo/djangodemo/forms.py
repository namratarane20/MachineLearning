from django.forms import ModelForm
from djangodemo.models import EmpData

class EmpolyeeDetailsForm(ModelForm):
    class Meta:
        model = EmpData
        fields = '__all__'
