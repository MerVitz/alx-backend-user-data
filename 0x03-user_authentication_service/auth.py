#!/usr/bin/env python3
"""
Auth class to handle user authentication and registration
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from werkzeug.security import generate_password_hash


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

    def get_user_from_session_id(self, session_id: str):
        """
        Find a user by their session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User: The User object corresponding found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session of a user by setting their session ID to None.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset token for the user corresponding to the email.
        
        Args:
            email (str): The email of the user requesting a password reset.
        
        Returns:
            str: A reset token for the user.
        
        Raises:
            ValueError: If no user with the provided email exists.
        """
        # Find the user corresponding to the email
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError("User DNE")
        # Generate a reset token (UUID)
        reset_token = str(uuid.uuid4())
        # Update the user's reset_token field
        user.reset_token = reset_token
        # Save the updated user object with the new reset_token
        self._db.save(user)
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Update the password for the user identified by the reset token.

        Args:
            reset_token (str): The reset token identifying the user.
            new_password (str): The new password to set for the user.

        Raises:
            ValueError: If the reset token is invalid or expired.
        """
        # Find user by reset_token
        user = self.get_user_by_reset_token(reset_token)

        if user is None:
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the user's password and reset_token field
        user.hashed_password = hashed_password
        user.reset_token = None
        self.save(user)
