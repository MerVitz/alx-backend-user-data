#!/usr/bin/env python3
""" Authentication class for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class to manage authentication for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path needs authentication, False if excluded """
        # If path is None or excluded_paths is None or empty, return True (requires auth)
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        # Strip trailing slashes for path and excluded paths
        path = path.rstrip('/')
        excluded_paths = [ep.rstrip('/') for ep in excluded_paths]
        # Return True if path is not in excluded_paths, meaning authentication is required
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Returns the Authorization header value if it exists, else None """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now, request will be used later """
        return None