from django.shortcuts import render
from rest_framework import generics
from testapp.models import Employee
from rest_framework.response import Response
from rest_framework.views import APIView
from testapp.serializers import EmployeeSerializer
# Create your views here.


class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        return Response(serializer.data)
