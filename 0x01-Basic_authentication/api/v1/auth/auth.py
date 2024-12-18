#!/usr/bin/env python3
""" Authentication class for the API with wildcard support """
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ Authentication class to manage authentication for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require auth.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Strip trailing slashes from path
        path = path.rstrip('/')
        
        # Check against all excluded paths
        for excluded_path in excluded_paths:
            # Remove trailing slashes and support wildcards
            if fnmatch.fnmatch(path, excluded_path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the Authorization header value if it exists, else None """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now, request will be used later """
        return None
