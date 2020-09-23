from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Employee
from .utils import valid_json
from .forms import EmployeeForm
import json
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeListCBV(View):
    def get(self, request, *args, **kwargs):
        qs = Employee.objects.all()
        json_data = serialize('json', qs, fields=('eno', 'ename'))
        pdict = json.loads(json_data)
        result = []
        for item in pdict:
            result.append(item['fields'])
        return HttpResponse(json.dumps(result), content_type='application/json')

    def post(self, request, *args, **kwargs):
        json_data = request.body
        if not valid_json(json_data):
            return HttpResponse(json.dumps({'msg': 'Please provide valid JSON data'}), status=404)
        form = EmployeeForm(json.loads(json_data))
        if form.is_valid():
            obj = form.save(commit=True)
            return HttpResponse(json.dumps({'msg': 'Sucessfully registeres'}), status=200)
        if form.errors:
            json_data = json.dumps(form.errors)
            return HttpResponse(json_data, status=404)


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
