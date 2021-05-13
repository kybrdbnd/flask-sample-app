from marshmallow import fields

from employee_management import ma
from employee_management.employee.models import Role, Asset


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class AssetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset


class EmployeeSchema(ma.Schema):
    # role = fields.Method('get_role')
    # assets = fields.Method('get_assets')

    class Meta:
        fields = ('id', 'name', 'email', 'role', 'assets')

    role = ma.Nested(RoleSchema)
    assets = ma.Nested(AssetSchema, many=True)


asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
employees_role_schema = EmployeeSchema(many=True, only=['id', 'name', 'email', 'role'])
employees_asset_schema = EmployeeSchema(many=True, only=['id', 'name', 'email', 'assets'])
employees_basic_schema = EmployeeSchema(many=True, only=['id', 'name', 'email'])
