import os
from flask import Flask
from flask_cognito import CognitoAuth
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

basedir = os.getcwd()
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'paper'

app.config.update({
    'COGNITO_REGION': 'ap-south-1',
    'COGNITO_USERPOOL_ID': os.environ.get('COGNITO_USERPOOL_ID'),
    'AWS_REGION_NAME': 'ap-south-1',
    'COGNITO_APP_CLIENT_ID': os.environ.get('COGNITO_APP_CLIENT_ID'),
    # client ID you wish to verify user is authenticated against
    'COGNITO_CHECK_TOKEN_EXPIRATION': False,  # disable token expiration checking for testing purposes
    'COGNITO_JWT_HEADER_NAME': 'Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer',
})

# sqlalchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)
cogauth = CognitoAuth(app)
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
