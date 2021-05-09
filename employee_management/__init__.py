from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

import os

basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)
manager = Manager(app)

from database import manager as database_manager

manager.add_command('db', MigrateCommand)
manager.add_command("database", database_manager)

from .employee import emp

app.register_blueprint(emp)
