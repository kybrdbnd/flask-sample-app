from flasgger import swag_from
from flask import jsonify
from . import emp
from .models import Employee, Role
from .schema import employees_schema, roles_schema


@emp.route('/employees')
@swag_from('docs/listEmployees.yml')
def list_employees():
    employees = Employee.query.all()
    return jsonify(employees_schema.dump(employees))


@emp.route('/roles')
@swag_from('docs/listRoles.yml')
def get_roles():
    roles = Role.query.all()
    return jsonify(roles_schema.dump(roles))
