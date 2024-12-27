#!/usr/bin/env python3
""" Authentication class for managing sessions"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User  # Import User model to fetch user data


class SessionAuth(Auth):
    """ Session authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id. """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves the User ID associated with a Session ID. """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Use dictionary's get method to fetch User ID
        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, session_id: str = None) -> bool:
        """ Deletes a session based on the Session ID. """
        if session_id is None or not isinstance(session_id, str):
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False

    def current_user(self, request=None):
        """
        Retrieves a User instance based on a session cookie value.
        """
        if request is None:
            return None

        # Retrieve the session ID from the request
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Retrieve the user ID from the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve and return the User instance
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout.
        """
        if request is None:
            return False

        # Retrieve session ID from request cookies
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Retrieve user ID for the session ID
        if not self.user_id_for_session_id(session_id):
            return False

        # Delete the session ID
        del self.user_id_by_session_id[session_id]
        return True
