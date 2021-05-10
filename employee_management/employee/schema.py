from employee_management import ma


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


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
