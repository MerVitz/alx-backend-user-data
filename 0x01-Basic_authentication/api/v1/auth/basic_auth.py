#!/usr/bin/env python3
"""
This module contains the BasicAuth class, which handles basic authentication.
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth. This class is responsible for 
    handling basic authentication logic, including extracting and decoding 
    Base64-encoded authorization headers.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.
        
        Args:
            authorization_header (str): The full Authorization header.
        
        Returns:
            str: The Base64 part after "Basic " if the header is valid.
            None: If the authorization_header is invalid.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith("Basic "):
            return None
        
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 authorization header into a UTF-8 string.
        
        Args:
            base64_authorization_header (str): The Base64 string to decode.
        
        Returns:
            str: The decoded string if successful.
            None: If the base64_authorization_header is invalid or cannot be decoded.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
