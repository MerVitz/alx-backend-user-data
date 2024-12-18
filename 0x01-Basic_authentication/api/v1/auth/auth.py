#!/usr/bin/env python3
""" Authentication class for the API
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Auth class to manage authentication for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if path is not in excluded_paths """
        
        # Return True if path is None
        if path is None:
            return True
        
        # Return True if excluded_paths is None or empty
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path to be slash-tolerant
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Normalize excluded paths to be slash-tolerant
            normalized_excluded_path = excluded_path if excluded_path.endswith('/') else excluded_path + '/'
            
            # If path is in excluded_paths, return False
            if normalized_path == normalized_excluded_path:
                return False
        
        # If path is not in excluded_paths, return True
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None for now, request will be used later """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now, request will be used later """
        return None
