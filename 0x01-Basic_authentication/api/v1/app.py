#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Check for environment variable to load the auth instance
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    auth = Auth()

@app.before_request
def before_request():
    """ Handle requests before processing """
    if auth is None:
        return None
    # Define routes that don’t require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    # If the current path requires authentication
    if request.path not in excluded_paths:
        # Check for valid authorization header
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized
        # Check if user is authenticated (current_user)
        if auth.current_user(request) is None:
            abort(403)  # Forbidden

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
