from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.getcwd()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

from .employee import emp
from .role import role

app.register_blueprint(emp)
app.register_blueprint(role)
