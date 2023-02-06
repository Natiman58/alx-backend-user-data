#!/usr/bin/env python3
"""
    Definition of basic authentication
"""
from re import A
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
        Template for basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
            returns the base64 part of authorization header
            for a basic authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        # if auth header doesn’t start by Basic (with a space at the end)
        if not authorization_header.startswith('Basic '):
                return None
        # Otherwise, return the value after Basic (after the space)
        return authorization_header.split(" ")[-1]

