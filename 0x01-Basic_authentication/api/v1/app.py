#!/usr/bin/env python3
"""
This module initializes the Flask app, registers blueprints, and handles
authentication based on the AUTH_TYPE environment variable. If AUTH_TYPE is 
set to 'basic_auth', it uses the BasicAuth class; otherwise, it uses the 
Auth class.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth


# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Check the environment variable AUTH_TYPE and assign the correct authentication class
if getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    auth = Auth()

@app.before_request
def before_request():
    """
    This function is executed before each request. It handles authentication 
    by checking if the request requires it and aborts with the appropriate 
    error code if necessary.
    """
    if auth is None:
        return None

    # List of routes that don't need authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # If the current path is in the excluded paths, bypass auth
    if request.path in excluded_paths:
        return None

    # Check if the route requires authentication
    if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized
        if auth.current_user(request) is None:
            abort(403)  # Forbidden

@app.errorhandler(404)
def not_found(error) -> str:
    """
    Error handler for 404 (Not Found) errors. 
    It returns a JSON response with the error message.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Error handler for 401 (Unauthorized) errors. 
    It returns a JSON response with the error message.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Error handler for 403 (Forbidden) errors. 
    It returns a JSON response with the error message.
    """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    """
    Run the Flask app on the specified host and port. The default host is 
    '0.0.0.0' and the default port is 5000.
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
