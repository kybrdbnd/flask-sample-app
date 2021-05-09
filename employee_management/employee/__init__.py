from flask import Blueprint

emp = Blueprint('employee', __name__, url_prefix='/employee')

from . import views
