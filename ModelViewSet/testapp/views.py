from django.shortcuts import render
from .serializers import EmployeeSerialzier
from .models import Employee
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class EmployeeCRUDCBV(ModelViewSet):
    serializer_class = EmployeeSerialzier
    queryset = Employee.objects.all()
