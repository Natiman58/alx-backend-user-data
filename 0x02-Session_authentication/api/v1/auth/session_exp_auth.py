#!/usr/bin/env python3
"""
    setting expiration date to a session ID
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv

SESSION_DURATION = int(getenv('SESSION_DURATION'))

class SessionExpAuth(SessionAuth):
    """
        handles the expiration date of the session
    """
    def __init__(self):
        """ initialize the class """
        if SESSION_DURATION is None:
            self.session_duration = 0
        self.session_duration = SESSION_DURATION

    def create_session(self, user_id=None):
        """
            create a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            creates user id using session id
        """
        if session_id is None:
            return None
        user_info = self.user_id_by_session_id.get(session_id)
        if user_info is None:
            return None
        if self.session_duration <= 0:
            return user_info.get("user_id")

        if "created_at" not in user_info.get("user_id"):
            return None
        created_at = user_info.get("created_at")
        allowed_time = created_at + timedelta(seconds=self.session_duration)
        if allowed_time < datetime.now():
            return None
        return user_info.get("user_id")


