#!/usr/bin/env python3
"""
    A simple flask application
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()  # create an instance of Auth class
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
        returns the message {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """
        registers a user using the username and password
        the user submitted; form data
    """
    # extract the value of the 'email' key from the form data
    email = request.form.get('email')

    # extract the password from the form data
    password = request.form.get('password')

    try:
        # registering the user using the email and password
        user = AUTH.register_user(email, password)
        # if the user is registered successfully, return the JSON response
        return jsonify({'email': f"{email}", 'message': "user created"})
    except ValueError:
        # if the user is already registered, return the JSON response & 400
        return jsonify({'message': "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
        handles th login request
    """
    # extract the email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')
    # check if it's a valid login session
    if AUTH.valid_login(email, password):
        # if it's a valid create a new session
        session_id = AUTH.create_session(email)
        # add the response
        response = make_response(jsonify({
                                          'email': email,
                                          'message': 'logged in'
                                          }))
        # store the session id as a cookie on the response
        response.set_cookie('session_id', session_id)
        return response
    # if not a valid session -> abort(401)
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
        handles the logout request
    """
    # extract the session id from the request
    session_id = request.cookies.get('session_id')
    # get the user using the session id
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # destroy the user
        AUTH.destroy_session(user.id)
        # redirect the response to the index page
        response = make_response(redirect('/'))
        # set session id cookie value to '' and cookie expire quickly
        response.set_cookie('session_id', '', expires=0)
        # and return the response
        return response
    # if no user return 403 HTTP status code
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
