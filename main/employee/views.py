from flasgger import swag_from
from flask import jsonify
from . import emp
from .models import Employee, employees_schema


@emp.route('/employees')
@swag_from('docs/listEmployees.yml')
def list_employees():
    employees = Employee.query.all()
    return jsonify(employees_schema.dump(employees))
