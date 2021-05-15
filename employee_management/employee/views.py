from flasgger import swag_from
from flask import jsonify, request
from flask_cognito import cognito_auth_required, cognito_group_permissions

from . import emp
from .controller.employeeController import (update_name_slug, authenticate_user, create_cognito_user,
                                            add_user_cognito_group, confirm_user)
from .models import Employee
from .schema import (employees_schema, employee_schema, employees_role_schema, employees_asset_schema)
from .. import db
from ..asset.models import Asset
from ..role.models import Role


@emp.route('/', methods=['POST', 'GET'])
@cognito_auth_required
@cognito_group_permissions(['hr'])
@swag_from('docs/employee_list.yml', methods=['GET'])
@swag_from('docs/employee_post.yml', methods=['POST'])
def list_create_employees():
    if request.method == 'GET':
        if 'includeFields' not in request.args:
            employees = Employee.query.with_entities(Employee.name, Employee.id, Employee.email)
            return jsonify(employees_schema.dump(employees))
        else:
            employees = Employee.query.all()
            isRole = False
            isAssets = False
            fields = request.args['includeFields'].split(',')
            for field in fields:
                field = field.strip(' ')
                if field == 'role':
                    isRole = True
                elif field == 'assets':
                    isAssets = True
            if isRole and isAssets is not True:
                return jsonify(employees_role_schema.dump(employees))
            elif isAssets and isRole is not True:
                return jsonify(employees_asset_schema.dump(employees))
            else:
                employees = Employee.query.all()
                return jsonify(employees_schema.dump(employees))

    if request.method == 'POST':
        data = request.json
        employeeJSON = {
            'name': None,
            'email': None,
            'roleId': None
        }
        if 'roleId' in data:
            employeeJSON['roleId'] = data['roleId']
        employeeJSON['name'] = data['name']
        employeeJSON['email'] = data['email']
        tempPassword = create_cognito_user(employeeJSON['email'])
        employee = Employee(name=employeeJSON['name'], email=employeeJSON['email'], roleId=employeeJSON['roleId'],
                            tempPassword=tempPassword)
        db.session.add(employee)
        db.session.commit()
        if employeeJSON['roleId'] is not None:
            roleName = Role.query.get(employeeJSON['roleId']).name
            add_user_cognito_group(employeeJSON['email'], roleName)
        return {"message": "employee created successfully",
                "tempPassword": tempPassword, "empId": employee.id}, 201


@emp.route('/<empId>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('docs/employee_get.yml', methods=['GET'])
@swag_from('docs/employee_delete.yml', methods=['DELETE'])
@swag_from('docs/employee_put.yml', methods=['PUT'])
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
            if 'name' in data:
                data = update_name_slug(data)
            employee.update(data)
            db.session.commit()
            return {"message": "employee updated successfully"}, 200
        else:
            return {"message": "employee not found"}, 404


@emp.route('/<empName>/search', methods=['GET'])
@swag_from('docs/employee_search.yml')
def employeeSearch(empName):
    employees = list(Employee.query.filter(Employee.nameSlug.contains(empName)))
    if len(employees) > 0:
        return jsonify(employees_schema.dump(employees)), 200
    else:
        return jsonify([]), 404


@emp.route('/<empId>/asset/<assetId>', methods=['PUT', 'DELETE'])
@swag_from('docs/employee_asset_put.yml', methods=['PUT'])
@swag_from('docs/employee_asset_delete.yml', methods=['DELETE'])
def employee_asset(empId, assetId):
    employee = Employee.query.get(empId)
    asset = Asset.query.get(assetId)
    if employee is None:
        return {"message": "employeeId not found"}, 404
    elif asset is None:
        return {"message": "asset not found"}, 404
    else:
        if request.method == 'PUT':
            if asset in employee.assets:
                return {"message": "asset already exists for an employee"}, 200
            else:
                employee.assets.append(asset)
                db.session.commit()
                return {"message": "asset successfully added to employee"}, 200
        if request.method == 'DELETE':
            employee.assets.remove(asset)
            db.session.commit()
            return {"message": "asset successfully removed from the employee"}, 200


@emp.route('/get_access_token', methods=['POST'])
@swag_from('docs/access_token.yml', methods=['POST'])
def get_access_token():
    data = request.json
    token = authenticate_user(data['email'], data['password'])
    return jsonify(token), 200


@emp.route('/reset_password', methods=['POST'])
@swag_from('docs/reset_password.yml', methods=['POST'])
def reset_password():
    data = request.json
    if 'tempPassword' in data and 'empId' in data and 'password' in data:
        tempPassword = data['tempPassword']
        empId = data['empId']
        employee = Employee.query.get(empId)
        if employee.tempPassword == tempPassword:
            confirm_user(employee.email, data['password'])
            return jsonify({"message": "password reset successfully done"}), 200
    else:
        return jsonify({"message": "provide tempPassword, password and empId"}), 200
