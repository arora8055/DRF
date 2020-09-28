from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from testapp.mixins import HttpResponseMixin, SerializeMixin
from testapp.utils import is_json
from testapp.forms import EmployeeForm
from testapp.models import Employee
import json
# Create your views here.

method_decorator(csrf_exempt, name='dispatch')


class EmployeeCRUDCBV(SerializeMixin, HttpResponseMixin, View):
    def get_object_by_id(self, id):
        try:
            s = Employee.objects.get(id)
        except Employee.DoesNotExist:
            s = None
        return s

    def get(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please send valid json only'}), status=400)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is not None:
            std = self.get_object_by_id(id)
            if std is None:
                return self.render_to_http_response(json.dumps({'msg': 'No match resource found'}), status=400)
            json_data = self.serialize([std, ])
            return self.render_to_http_response(json_data)
        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please send valid js only'}), status=400)
        emp_data = json.loads(data)
        form = EmployeeForm(emp_data)
        if form.is_valid():
            form.save(commit=True)
            return self.render_to_http_response(json.dumps({'msg': 'Resource Created Sucessfully'}))
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)

    # def put(self, request, *args, **kwargs):
