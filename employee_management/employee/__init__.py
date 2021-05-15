from flask import Blueprint

emp = Blueprint('employee_bp', __name__, url_prefix='/employee')

from . import views
