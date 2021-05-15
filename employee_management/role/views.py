from flasgger import swag_from
from flask import request, jsonify

from employee_management import db
from employee_management.employee.schema import employees_basic_schema
from employee_management.role.models import Role
from employee_management.role.schema import roles_schema
from . import role


@role.route('/', methods=['GET', 'POST'])
@swag_from('docs/role_list.yml', methods=['GET'])
@swag_from('docs/role_post.yml', methods=['POST'])
def emp_roles():
    if request.method == 'GET':
        roles = Role.query.all()
        return jsonify(roles_schema.dump(roles))
    if request.method == 'POST':
        data = request.json
        try:
            role = Role(name=data['name'])
            db.session.add(role)
            db.session.commit()
            return {"message": "Role created successfully"}, 201
        except Exception as err:
            return {"message": str(err)}, 500


@role.route('/roles/<roleId>', methods=['PUT', 'DELETE'])
@swag_from('docs/role_delete.yml', methods=['DELETE'])
@swag_from('docs/role_put.yml', methods=['PUT'])
def roles_update(roleId):
    if request.method == 'PUT':
        if Role.query.get(roleId):
            role = Role.query.filter_by(id=roleId)
            data = request.json
            role.update(data)
            db.session.commit()
            return {"message": "role updated successfully"}, 200
        else:
            return {"message": "role not found"}, 404
    if request.method == 'DELETE':
        role = Role.query.get(roleId)
        if role is not None:
            db.session.delete(role)
            db.session.commit()
            return {}, 204
        else:
            return {"message": "role not found"}, 404


@role.route('/roles/<roleId>/employees', methods=['GET'])
@swag_from('docs/role_employees.yml', methods=['GET'])
def role_employees(roleId):
    role = Role.query.get(roleId)
    return jsonify(employees_basic_schema.dump(role.employees)), 200
