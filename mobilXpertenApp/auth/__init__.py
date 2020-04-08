from flask import Blueprint

bp = Blueprint('auth', __name__)

from mobilXpertenApp.auth import routes