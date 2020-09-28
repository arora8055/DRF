from testapp.models import Employee
from django import forms


class EmployeeForm(forms.ModelForm):
    def clean_data(self):
        input_marks = self.cleaned_data['marks']
        if input_marks < 35:
            raise forms.ValidationError(
                'Employee marks must be greater than 35')

    class Meta:
        model = Employee
        fields = '__all__'
