#!/usr/bin/env python3
"""
    A simple flask application
"""
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
        returns the message {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
