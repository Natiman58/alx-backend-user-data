#!/usr/bin/env python3
"""
    A simple flask application
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
