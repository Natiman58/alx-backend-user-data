#!/usr/bin/env python3
"""
    a class to manage the API authentication.
"""

import re
from typing import List, TypeVar
from flask import request


class Auth:
    """
        A template for all authentications
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determines which routs need authentication
        path: path to be checked for authentication
        excluded_paths: list of paths that don't require authentication

        returns: True is path is in excluded_paths
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path) or path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        validate all requests to secure the API
        returns authorization header from the request
        """
        if request is None:
            return None

        # header key: Authorization
        header_key = request.headers.get('Authorization')
        # if the request doesn't contain header key; -> None
        if header_key is None:
            return None

        return header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """ """
        return None
