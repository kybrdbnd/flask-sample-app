from flask import Blueprint

asset = Blueprint('asset', __name__, url_prefix='/asset')

from . import views
