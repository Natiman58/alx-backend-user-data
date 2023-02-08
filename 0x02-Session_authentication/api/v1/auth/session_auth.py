#!/usr/bin/env python3
"""
    A module that implements session authentication
"""
from uuid import uuid4

from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            returns user id besed on the session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
            returns current user instance based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)

        return user
