from flask import Blueprint

asset = Blueprint('asset_bp', __name__, url_prefix='/asset')

from . import views
