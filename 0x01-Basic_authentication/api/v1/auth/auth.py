#!/usr/bin/env python3
""" Authentication class for the API
"""
from flask import request
from typing import List, TypeVar

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