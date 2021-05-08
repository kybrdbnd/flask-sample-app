from flask import Blueprint

emp = Blueprint('employee', __name__)

from . import views
