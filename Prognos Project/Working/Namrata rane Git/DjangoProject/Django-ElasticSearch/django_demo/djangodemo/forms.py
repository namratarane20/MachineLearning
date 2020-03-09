from django.forms import ModelForm
from djangodemo.models import EmpolyeeDetails

class EmpolyeeDetailsForm(ModelForm):
    class Meta:
        model = EmpolyeeDetails
        fields = '__all__'
