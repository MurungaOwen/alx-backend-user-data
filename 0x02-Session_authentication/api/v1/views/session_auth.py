#!/usr/bin/env python3
"""module for views of session auth"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
    '/auth_session/login',  methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """Handles user login with session authentication."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) is 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) is 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)

    session_name = getenv('SESSION_NAME')
    response = jsonify(user[0].to_json())
    response.set_cookie(session_name, session_id)

    return response