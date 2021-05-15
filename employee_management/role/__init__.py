from flask import Blueprint

role = Blueprint('role_bp', __name__, url_prefix='/role')

from . import views
