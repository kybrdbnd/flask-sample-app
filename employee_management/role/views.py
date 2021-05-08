from flasgger import swag_from
from flask import jsonify
from . import role
from .models import Role, roles_schema


@role.route('/roles')
@swag_from('docs/listRoles.yml')
def get_roles():
    roles = Role.query.all()
    return jsonify(roles_schema.dump(roles))
