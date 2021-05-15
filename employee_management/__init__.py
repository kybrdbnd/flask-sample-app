from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_script import Manager
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


@app.route('/')
def welcome():
    return {
        "message": "this is a sample api for flutter application"
    }


from .employee import emp
from .asset import asset
from .role import role

app.register_blueprint(emp)
app.register_blueprint(asset)
app.register_blueprint(role)
