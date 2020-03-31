from flask import Blueprint

bp = Blueprint('api', __name__)

from mobilXpertenApp.api import users, devices, repairs, errors