#!/usr/bin/env python3
"""
Flask app to handle user registration and login.
"""

from flask import Flask, request, jsonify, abort, make_response,redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """
    Root route.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Register a new user.

    Expects:
        - email: str (form data)
        - password: str (form data)

    Returns:
        JSON response with appropriate message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Log in a user and create a new session.

    Expects:
        - email: str (form data)
        - password: str (form data)

    Returns:
        JSON response with appropriate message and sets session_id as a cookie.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)  # Unauthorized

    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized

    # Create a session for the user
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)  # Unauthorized

    # Set the session_id as a cookie in the response
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Log out a user by destroying their session.

    Expected:
        - session_id: Cookie containing the session ID.

    Returns:
        - Redirects to the root route if successful.
        - Responds with 403 if the session ID is invalid.
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        abort(403)

    # Find the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403)
    
    # Destroy the session and redirect to "/"
    AUTH.destroy_session(user.id)
    return redirect("/")

@app.route("/profile", methods=["GET"])
def profile():
    """
    Retrieve the user's profile.

    Expects:
        - session_id: Cookie containing the session ID.

    Returns:
        JSON response with user email if the session ID is valid.
        Returns 403 status if the session is invalid or not found.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        return jsonify({"message": "Forbidden"}), 403  # No session ID provided

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        return jsonify({"message": "Forbidden"}), 403  # Invalid session ID

    return jsonify({"email": user.email})

@app.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Handle the POST request to generate a reset password token.
    
    Expects:
        - email: str (form data)

    Returns:
        JSON response containing the reset token or a 403 error if the email is not registered.
    """
    email = request.form.get("email")
    
    if not email:
        return jsonify({"message": "Email required"}), 400

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return jsonify({"message": "Forbidden"}), 403

@app.route("/reset_password", methods=["PUT"])
def update_password_endpoint():
    """
    Handle the PUT request to update the user's password using a reset token.
    
    Expects:
        - email: str (form data)
        - reset_token: str (form data)
        - new_password: str (form data)
    
    Returns:
        JSON response confirming the update or a 403 error if the token is invalid.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    
    if not email or not reset_token or not new_password:
        return jsonify({"message": "Missing fields"}), 400
    
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Forbidden"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
