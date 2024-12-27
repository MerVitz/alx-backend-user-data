#!/usr/bin/env python3
"""
Session Authentication view
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    POST /api/v1/auth_session/login
    Handles user login using session authentication.
    """
    # Retrieve email and password
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Set the session ID in the response cookie
    session_name = os.getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response
