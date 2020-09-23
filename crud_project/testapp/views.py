from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Employee
import json
# Create your views here.


class EmployeeListCBV(View):
    def get(self, request, *args, **kwargs):
        qs = Employee.objects.all()
        json_data = serialize('json', qs, fields=('eno', 'ename'))
        pdict = json.loads(json_data)
        result = []
        for item in pdict:
            result.append(item['fields'])
        return HttpResponse(json.dumps(result), content_type='application/json')


class EmployeeDetailCBV(View):
    def get(self, request, id, *args, **kwargs):
        try:
            emp_data = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return HttpResponse(json.dumps({'msg': 'User Not Found'}), status=404)
        else:
            json_data = serialize(
                'json', [emp_data, ], fields=('eno', 'ename'))
            pdict = json.loads(json_data)
            result = []
            for item in pdict:
                result.append(item['fields'])
            return HttpResponse(json.dumps(result), content_type='application/json')
