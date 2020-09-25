from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.core.serializers import serialize
import json
from .models import Employee
from .utils import valid_json
# Create your views here.


class EmployeeCRUDCBV(View):
    def get(self, request, *args, **kwargs):
        data = request.body
        if not valid_json(data):
            return HttpResponse(json.dumps({'msg': 'Please provide valid JSON'}))
        data = json.loads(data)
        # id = json.loads(data).get('id', None)
        # if id is not None:
        #     try:
        #         obj = Employee.objects.get(id)
        #     except Employee.DoesNotExist:
        #         return HttpResponse(json.dumps({'msg': 'No data found'}))
        #     else:
        #         json_data = serialize('json', [obj, ])
        #         result = []
        #         for item in json_data:
        #             result.append(json_data['fields'])
        #         return HttpResponse(json.dumps(result))
        # else:
        #     qs = Employee.objects.all()
        #     json_data = serialize('json', qs)
        #     result = []
        #     for item in json_data:
        #         result.append(json_data['fields'])
        #     return HttpResponse(json.dumps(result))
