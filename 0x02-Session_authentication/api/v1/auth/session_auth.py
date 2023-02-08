#!/usr/bin/env python3
"""
    A module that implements session authentication
"""
from uuid import uuid4
from .auth import Auth

class SessionAuth(Auth):
    """
        for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session id for a user
        using user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
