#!/usr/bin/env python3
"""
    a class to manage the API authentication.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
        A template for all authentications
    """    

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ """
        return False
    
    def authorization_header(self, request=None) -> str:
        """ """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ """
        return None