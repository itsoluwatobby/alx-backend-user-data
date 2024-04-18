#!/usr/bin/env python3
"""
session_auth view
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
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
                res = jsonify(user.to_json())
                res.set_cookie(getenv('SESSION_NAME'), session_id)
                return res
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Session logout authentication"""
    from api.v1.app import auth
    session_ended = auth.destroy_session(request)
    if session_ended is False:
        abort(404)
        return False
    return jsonify({}), 200
