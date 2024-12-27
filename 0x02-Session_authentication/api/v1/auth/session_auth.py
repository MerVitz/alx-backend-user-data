#!/usr/bin/env python3
""" Authentication class for managing sessions"""
import uuid
from api.v1.auth.auth import Auth


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
