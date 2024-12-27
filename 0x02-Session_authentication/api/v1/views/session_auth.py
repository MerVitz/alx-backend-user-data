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
    try:
        users = User.search({"email": email})
    except Exception as e:
        print(f"Error in User search: {e}")
        return jsonify({"error": "internal server error"}), 500

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    try:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    except Exception as e:
        print(f"Error validating password: {e}")
        return jsonify({"error": "internal server error"}), 500

    # Create a session ID for the user
    try:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
    except Exception as e:
        print(f"Error creating session: {e}")
        return jsonify({"error": "internal server error"}), 500

    # Set the session ID in the response cookie
    session_name = os.getenv('SESSION_NAME')
    if not session_name:
        print("SESSION_NAME environment variable is not set.")
        return jsonify({"error": "server configuration error"}), 500

    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response
