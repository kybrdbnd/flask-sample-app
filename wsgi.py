import json

from flasgger import Swagger
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from employee_management import app, manager, db
from employee_management.asset.models import Asset
from employee_management.employee.models import Employee
from employee_management.role.models import Role

with open('configs/app_config.json', 'r') as f:
    template = json.load(f)
with open('configs/swagger_config.json', 'r') as f:
    swagger_config = json.load(f)

if __name__ == "__main__":
    swagger = Swagger(app, template=template, config=swagger_config)
    admin = Admin(app, name='Employee Management', template_mode='bootstrap3')
    admin.add_view(ModelView(Employee, db.session))
    admin.add_view(ModelView(Asset, db.session))
    admin.add_view(ModelView(Role, db.session))

    manager.run()
