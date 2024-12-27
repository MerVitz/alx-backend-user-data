#!/usr/bin/env python3
"""
This module initializes the Flask app, registers blueprints, and handles
authentication based on the AUTH_TYPE environment variable. It supports
BasicAuth and SessionAuth mechanisms.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Check the environment variable AUTH_TYPE and assign the correct
# authentication class
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """Filter each request with authentication"""
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


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
