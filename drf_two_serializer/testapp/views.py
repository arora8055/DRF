from django.shortcuts import render
from django.views.generic import View
from testapp.models import Employee
from testapp.serializers import EmployeeSerializer
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCRUBCBV(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id', None)
        if id is not None:
            emp = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(emp)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        # import pdb
        # pdb.set_trace()
        data = JSONParser().parse(stream)
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg = {'msg': 'Resource created successfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        emp = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(emp, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {'msg': 'Resource updated sucessfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')
