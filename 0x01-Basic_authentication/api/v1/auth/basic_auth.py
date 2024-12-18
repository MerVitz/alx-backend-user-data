#!/usr/bin/env python3
"""
This module contains the BasicAuth class, which implements Basic Authentication
for an API, including methods to extract user credentials, validate passwords,
and retrieve user objects based on credentials.
"""

import base64
from models.user import User
from typing import TypeVar


class BasicAuth:
    """
    BasicAuth class for Basic Authentication.

    This class provides methods to extract and validate user credentials from
    an authorization header and retrieve
    the corresponding user from the database.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the
        authorization header for Basic Authentication.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The Base64 encoded part of the header, or None if invalid.
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str):
            The Base64 encoded authorization header.

        Returns:
            str: The decoded authorization header, or None if invalid.
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user credentials
        (email and password) from the decoded Base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str):
            The decoded authorization header.

        Returns:
            tuple: A tuple containing the user email
            and password, or (None, None) if invalid.
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(":", 1)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the user object based on email and password credentials.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The user object if credentials are valid, or None if invalid.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        user = User.search(user_email)
        if user is None:
            return None

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request's authorization header.

        Args:
            request: The HTTP request object containing
            the authorization header.

        Returns:
            User: The user object if authentication is successful,
            or None if not authenticated.
        """
        if request is None:
            return None

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        if not base64_authorization_header:
            return None

        decoded_base64_authorization_header = (
                self.decode_base64_authorization_header(
                    base64_authorization_header))
        if not decoded_base64_authorization_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
