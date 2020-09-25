from django.shortcuts import render
from django.views.generic import View
from .models import Employee
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from testapp.mixins import SerializeMixin, HttpResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from testapp.utils import is_json
from testapp.forms import EmployeeForm
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCRUDCBV(HttpResponseMixin, SerializeMixin, View):
    def get_object_by_id(self, id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, *args, **kwargs):
        data = request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg': 'plz send valid json data only'}), status=400)
        data = json.loads(data)
        id = data.get('id', None)
        if id is not None:
            obj = self.get_object_by_id(id)
            if obj is None:
                return self.render_to_http_response(json.dumps({'msg': 'No Matched Record Found with Specified Id'}), status=404)
            json_data = self.serialize([obj, ])
            return self.render_to_http_response(json_data)
        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self, request, *args, **kwargs):
        data = request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg': 'plz send valid json data only'}), status=400)
        empdata = json.loads(request.body)
        form = EmployeeForm(empdata)
        if form.is_valid():
            obj = form.save(commit=True)
            return self.render_to_http_response(json.dumps({'msg': 'resource created successfully'}))
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)
