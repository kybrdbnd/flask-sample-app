from flask import Blueprint

role = Blueprint('role', __name__, url_prefix='/role')

from . import views
