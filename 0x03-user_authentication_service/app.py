#!/usr/bin/env python3
"""
app module
"""
from flask import Flask, abort, request, jsonify, redirect
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """User login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not Auth.valid_login(email, password):
        abort(401)
    else:
        session_id = Auth.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """User logout route"""
    session_id = request.cookie.get('session_id')
    try:
        Auth.


if __name__ == "__main__":
    """Runs flask app"""
    app.run(host="0.0.0.0", port="5000")
