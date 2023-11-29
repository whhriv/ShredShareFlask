from flask import jsonify
from app import db
from app.api import api
from app.api.auth import basic_auth
from app.api.auth import token_auth

@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

# @api.route('/deletetokens', methods=['DELETE'])
# @token_auth.login_required
# def revoke_token():
#     token_auth.current_user().revoke_token()
#     db.session.commit()
#     return '', 204