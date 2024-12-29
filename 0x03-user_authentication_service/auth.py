#!/usr/bin/env python3
"""
Hashing passowrd
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt and return the salted hash.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt with a default work factor (e.g., 12)
    salt = bcrypt.gensalt(rounds=12)
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password