from employee_management import ma
from employee_management.asset.schema import AssetSchema
from employee_management.role.schema import RoleSchema


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'role', 'assets')

    role = ma.Nested(RoleSchema)
    assets = ma.Nested(AssetSchema, many=True)


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
employees_role_schema = EmployeeSchema(many=True, only=['id', 'name', 'email', 'role'])
employees_asset_schema = EmployeeSchema(many=True, only=['id', 'name', 'email', 'assets'])
employees_basic_schema = EmployeeSchema(many=True, only=['id', 'name', 'email'])
