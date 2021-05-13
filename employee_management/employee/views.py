from flasgger import swag_from
from flask import jsonify, request

from . import emp
from .controller.employeeController import update_name_slug
from .models import Employee, Role, Asset
from .schema import employees_schema, roles_schema, assets_schema, employee_schema, asset_schema, employees_role_schema, \
    employees_asset_schema, employees_basic_schema
from .. import db


@emp.route('/', methods=['POST', 'GET'])
@swag_from('docs/employee/employee_list.yml', methods=['GET'])
@swag_from('docs/employee/employee_post.yml', methods=['POST'])
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
        employee = Employee(name=employeeJSON['name'], email=employeeJSON['email'], roleId=employeeJSON['roleId'])
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
            if 'name' in data:
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


@emp.route('/<empId>/asset/<assetId>', methods=['PUT', 'DELETE'])
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


@emp.route('/roles', methods=['GET', 'POST'])
@swag_from('docs/role/role_list.yml', methods=['GET'])
@swag_from('docs/role/role_post.yml', methods=['POST'])
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


@emp.route('/roles/<roleId>/employees', methods=['GET'])
@swag_from('docs/role/role_employees.yml', methods=['GET'])
def role_employees(roleId):
    role = Role.query.get(roleId)
    return jsonify(employees_basic_schema.dump(role.employees)), 200


@emp.route('/assets', methods=['GET', 'POST'])
@swag_from('docs/asset/asset_list.yml', methods=['GET'])
@swag_from('docs/asset/asset_post.yml', methods=['POST'])
def emp_assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        return jsonify(assets_schema.dump(assets))
    if request.method == 'POST':
        data = request.json
        try:
            asset = Asset(name=data['name'])
            db.session.add(asset)
            db.session.commit()
            return {"message": "asset created successfully"}, 201
        except Exception as err:
            return {"message": str(err)}, 500


@emp.route('/assets/<assetId>', methods=['GET', 'PUT', 'DELETE'])
@swag_from('docs/asset/asset_get.yml', methods=['GET'])
@swag_from('docs/asset/asset_put.yml', methods=['PUT'])
@swag_from('docs/asset/asset_delete.yml', methods=['DELETE'])
def assets_crud(assetId):
    if request.method == 'GET':
        asset = Asset.query.get(id=assetId)
        if asset is not None:
            return jsonify(asset_schema.dump(asset)), 200
        else:
            return {"message": "asset not found"}, 404
    if request.method == 'DELETE':
        asset = Asset.query.get(assetId)
        if asset is not None:
            db.session.delete(asset)
            db.session.commit()
            return {}, 204
        else:
            return {"message": "asset not found"}, 404
    if request.method == 'PUT':
        if Asset.query.get(assetId):
            asset = Asset.query.filter_by(id=assetId)
            data = request.json
            asset.update(data)
            db.session.commit()
            return {"message": "asset updated successfully"}, 200
        else:
            return {"message": "asset not found"}, 404
