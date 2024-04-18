#!/usr/bin/env python3
"""
session_auth view
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Session login authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        # if not users:
        #    return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                res = make_response(user.to_json())
                res.set_cookie(getenv('SESSION_NAME', session_id))
                return res
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404
