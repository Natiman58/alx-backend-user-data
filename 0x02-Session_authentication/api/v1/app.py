#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()


excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/',
            ]


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
        unauthorized handler
        handles 401 error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
        Forbidden error handler
        403 error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
        filter each request
        before they are handeled
    """
    if auth is None:
        pass
    else:
        # if path requires authentication
        if auth.require_auth(request.path, excluded):
            # if request doesn't have header key: "Authorization" and
            # cookie is empty -> 401 abort request
            header_key = auth.authorization_header(request)
            cookie = auth.session_cookie(request)
            if header_key is None and cookie is None:
                abort(401, description="Unauthorized")
            # If current user returns None -> 403(Forbidden)
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")
            else:
                request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
