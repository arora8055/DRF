from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Employee
import json
# Create your views here.


class EmployeeDetailCBV(View):
    def get(self, request):
        qs = Employee.objects.all()
        json_data = serialize('json', qs, fields=('eno', 'ename'))
        pdict = json.loads(json_data)
        result = []
        for item in pdict:
            result.append(item['fields'])
        return HttpResponse(json.dumps(result), content_type='application/json')
