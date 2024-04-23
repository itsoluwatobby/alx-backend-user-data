#!/usr/bin/env python3
"""
app module
"""
from flask import Flask, request, jsonify
from auth import Auth


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """User registration route"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = Auth.register_user(email, password)
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": user.email, "message": "user created"})


#@app.route('/users', methods=['POST'], strict_slashes=False)
#def users():
#    """User registration route"""


if __name__ == "__main__":
    """Runs flask app"""
    app.run(host="0.0.0.0", port="5000")
