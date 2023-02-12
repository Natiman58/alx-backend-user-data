#!/usr/bin/env python3
"""
    a module for user db authentication 
"""
from asyncio import FastChildWatcher
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
        A class for user db authentication
    """
    def create_session(self, user_id=None):
        """
            creates a new session using the given user_id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_dict = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**user_dict)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            returns the user id for the given session_id
        """
        user_id = UserSession.search({"session_id": session_id})
        if not user_id:
            return None
        return user_id

    def destroy_session(self, request=None):
        """
            deletes the UserSession based the session_id
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        print(session_id)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
