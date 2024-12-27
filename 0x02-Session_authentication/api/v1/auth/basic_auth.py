#!/usr/bin/env python3
"""
This module contains the BasicAuth class, which implements Basic Authentication
for an API, including methods to extract user credentials, validate passwords,
and retrieve user objects based on credentials.
"""

import base64
from typing import TypeVar, Tuple
from models.user import User


class BasicAuth:
    """
    BasicAuth class for Basic Authentication.

    Provides methods to extract user credentials from the Authorization header,
    validate them, and retrieve the associated User instance.
    """

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The HTTP request object.

        Returns:
            str: The Authorization header value, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Determine if authentication is required for a given path.
        :param path: The requested path.
        :param excluded_paths: List of paths that don't require authentication.
        :return: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        # Normalize paths
        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):  # wildcard matching
                if path.startswith(excluded_path[:-1]):
                    return False
            if path == excluded_path.rstrip('/'):
                return False
        return True

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the authorization header for Basic Auth.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The Base64 encoded part of the header, or None if invalid.
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded authorization
            header.

        Returns:
            str: The decoded authorization header, or None if invalid.
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header
            ).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        Extracts the user credentials from the decoded Base64 header.

        Args:
            decoded_base64_authorization_header (str): The decoded header.

        Returns:
            Tuple[str, str]: The user email and password, or (None, None).
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.
        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.
        Returns:
            User: The user instance if credentials are valid, or None.
        """
        # Validate inputs
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # Search for the user using the email
        users = User.search({"email": user_email})
        if not users or len(users) == 0:  # No users found
            return None

        # Check the first user (assuming only one match for the email)
        user = users[0]
        if not user.is_valid_password(user_pwd):  # Password does not match
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request's Authorization header.
        Args:
            request: The HTTP request object
            containing the Authorization header.
        Returns:
            User: The authenticated user instance,
            or None if authentication fails.
        """
        if request is None:
            return None

        # Extract the Authorization header from the request
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        # Extract and decode the Base64 part of the Authorization header
        base64_header = self.extract_base64_authorization_header(auth_header)
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        # Extract user credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if not user_email or not user_pwd:
            return None

        # Retrieve the user object using the extracted credentials
        return self.user_object_from_credentials(user_email, user_pwd)
