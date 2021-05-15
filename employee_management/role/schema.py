from employee_management import ma
from employee_management.role.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
