from django.shortcuts import render
from rest_framework import generics
from testapp.models import Employee
from rest_framework.response import Response
from rest_framework.views import APIView
from testapp.serializers import EmployeeSerializer
# Create your views here.


class EmployeeAPIView(generics.ListAPIView):
    # queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        qs = Employee.objects.all()
        # import pdb
        # pdb.set_trace()
        name = self.request.GET.get('ename')
        if name is not None:
            qs = qs.filter(ename__icontains=name)
        return qs


class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
