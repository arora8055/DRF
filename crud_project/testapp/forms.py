from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    def clean_esal(self):
        input = self.cleaned_data['esal']
        if input < 5000:
            raise forms.ValidationError('Val must be greater thn 5000')
        return input

    class Meta:
        model = Employee
        fields = '__all__'
