#!/usr/bin/env python3
"""
Auth class to handle user authentication and registration
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError


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


def _generate_uuid() -> str:
    """
    Generate a new UUID string.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth class with an instance of DB."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the database.

        Args:
            email (str): The email address for the new user.
            password (str): The password for the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user already exists with the given email.
        """
        # Check if the user already exists
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except InvalidRequestError:
            # If no user is found, proceed with creating the new user
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Add the new user to the database
        # Ensure the password is stored as a string
        user = self._db.add_user(email, hashed_password.decode('utf-8'))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate if the provided email and password match a user.

        Args:
            email (str): The email address of the user.
            password (str): The password to validate.

        Returns:
            bool: True if valid login, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            # Check the password against the stored hashed password
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8'))
        except Exception:
            # Return False if any error occurs (user not found, etc.)
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user with the provided email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The new session ID, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            # Generate a new session ID
            session_id = _generate_uuid()
            # Update the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None
