from marshmallow import fields

from employee_management import ma
from employee_management.employee.models import Role


class EmployeeSchema(ma.Schema):
    roleName = fields.Method('get_role_name')

    @staticmethod
    def get_role_name(obj):
        name = None
        if obj.roleId is not None:
            role = Role.query.get(obj.roleId)
            if role is not None:
                name = role.name
        return name

    class Meta:
        fields = ('id', 'name', 'email', 'roleId', 'roleName')


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class AssetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
