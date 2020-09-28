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

    def put(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please send valid js only'}), status=400)
        provided_data = json.loads(data)
        id = provided_data.get('id', None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg': 'To perform updation id is mandatory,plz provide id'}), status=400)
        std = self.get_object_by_id(id)
        original_data = {
            'name': std.name,
            'rollno': std.rollno,
            'marks': std.marks
        }
        original_data.update(provided_data)
        form = EmployeeForm(original_data, instance=std)
        if form.is_valid():
            form.save(commit=True)
            return self.render_to_http_response(json.dumps({'msg': 'Resource UpdatedSuccessfully'}))
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)

    def delete(self, request, *args, **kwargs):
        data = request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg': 'plz send valid jsondata only'}), status=400)
        data = json.loads(request.body)
        id = data.get('id', None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg': 'To perform delete,id is mandatory,you should provide'}), status=400)
        obj = self.get_object_by_id(id)
        if obj is None:
            json_data = json.dumps(
                {'msg': 'No matched record found, Not possible to perform delete operation'})
            return self.render_to_http_response(json_data, status=404)
        status, deleted_item = obj.delete()
        if status == 1:
            json_data = json.dumps({'msg': 'Resource Deleted successfully'})
            return self.render_to_http_response(json_data)
        json_data = json.dumps({'msg': 'unable to delete ...plz try again'})
        return self.render_to_http_response(json_data, status=500)
