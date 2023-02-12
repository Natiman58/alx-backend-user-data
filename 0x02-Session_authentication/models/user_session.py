#!/usr/bin/env python3
"""
    A user session model
"""
from .base import Base


class UserSession(Base):
    """
        A class representing the user session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
            initialize the session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
