#!/usr/bin/env python3
"""
    session authentication provider
"""

from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from os import abort, getenv
SESSION_Name = getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
        handles the login session
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pwd is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if users == [] or not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        dict_user = make_response(jsonify(user.to_json()))
        dict_user.set_cookie(SESSION_Name, session_id)
        return dict_user

    @app_views.route('/auth_session/logout',
                     methods=['DELETE'],
                     strict_slashes=False)
    def logout():
        """logging out and destroy session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
