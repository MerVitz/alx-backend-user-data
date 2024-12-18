#!/usr/bin/env python3
""" Authentication class for the API
"""
from typing import List, TypeVar
from flask import request
from flask import request  # !/usr/bin/env python3
""" Authentication class for the API
"""


class Auth:
    """ Auth class to manage authentication for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if path is not in excluded_paths """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path to be slash-tolerant
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Normalize excluded paths to be slash-tolerant
            normalized_excluded_path = excluded_path if excluded_path.endswith(
                '/') else excluded_path + '/'
            if normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None for now, request will be used later """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now, request will be used later """
        return None


class Auth:
    """ Auth class to manage authentication for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False, path and excluded_paths will be used later """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None for now, request will be used later """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now, request will be used later """
        return None
