from flasgger import swag_from
from flask import jsonify, request
from . import emp
from .controller.employeeController import update_name_slug
from .models import Employee, Role, Asset
from .schema import employees_schema, roles_schema, assets_schema, employee_schema
from .. import db


@emp.route('/', methods=['POST', 'GET'])
@swag_from('docs/employee/employee_list.yml', methods=['GET'])
@swag_from('docs/employee/employee_post.yml', methods=['POST'])
def list_create_employees():
    if request.method == 'GET':
        employees = Employee.query.all()
        return jsonify(employees_schema.dump(employees))
    if request.method == 'POST':
        data = request.json
        employee = Employee(data['name'], data['email'])
        db.session.add(employee)
        db.session.commit()
        return {"message": "employee created successfully"}, 201


@emp.route('/<empId>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('docs/employee/employee_get.yml', methods=['GET'])
@swag_from('docs/employee/employee_delete.yml', methods=['DELETE'])
@swag_from('docs/employee/employee_put.yml', methods=['PUT'])
def employeesCrud(empId):
    if request.method == 'GET':
        employee = Employee.query.get(empId)
        if employee is None:
            return {"message": "employee not found"}, 404
        return jsonify(employee_schema.dump(employee))
    if request.method == 'DELETE':
        employee = Employee.query.get(empId)
        if employee is not None:
            db.session.delete(employee)
            db.session.commit()
            return {}, 204
        else:
            return {"message": "employee not found"}, 404
    if request.method == 'PUT':
        if Employee.query.get(empId):
            employee = Employee.query.filter_by(id=empId)
            data = request.json
            data = update_name_slug(data)
            employee.update(data)
            db.session.commit()
            return {"message": "employee updated successfully"}, 200
        else:
            return {"message": "employee not found"}, 404


@emp.route('/<empName>/search', methods=['GET'])
@swag_from('docs/employee/employee_search.yml')
def employeeSearch(empName):
    employees = list(Employee.query.filter(Employee.nameSlug.contains(empName)))
    if len(employees) > 0:
        return jsonify(employees_schema.dump(employees)), 200
    else:
        return jsonify([]), 404


@emp.route('/roles', methods=['GET', 'POST'])
@swag_from('docs/role/role_list.yml', methods=['GET'])
@swag_from('docs/role/role_post.yml', methods=['POST'])
def emp_roles():
    if request.method == 'GET':
        roles = Role.query.all()
        return jsonify(roles_schema.dump(roles))
    if request.method == 'POST':
        data = request.json
        role = Role(data['name'])
        db.session.add(role)
        db.session.commit()
        return {"message": "Role created successfully"}, 201


@emp.route('/roles/<roleId>', methods=['PUT', 'DELETE'])
@swag_from('docs/role/role_delete.yml', methods=['DELETE'])
@swag_from('docs/role/role_put.yml', methods=['PUT'])
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


@emp.route('/assets', methods=['GET', 'POST'])
@swag_from('docs/asset/asset_list.yml', methods=['GET'])
@swag_from('docs/asset/asset_post.yml', methods=['POST'])
def emp_assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        return jsonify(assets_schema.dump(assets))
    if request.method == 'POST':
        data = request.json
        asset = Asset(data['name'])
        db.session.add(asset)
        db.session.commit()
        return {"message": "asset created successfully"}, 201
