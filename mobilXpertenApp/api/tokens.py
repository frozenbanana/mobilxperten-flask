from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from mobilXpertenApp import db
from mobilXpertenApp.api import bp
from mobilXpertenApp.api.auth import basic_auth, token_auth

basic_auth = HTTPBasicAuth()

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204