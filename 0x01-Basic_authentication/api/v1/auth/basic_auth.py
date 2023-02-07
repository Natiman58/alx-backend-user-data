#!/usr/bin/env python3
"""
    Definition of basic authentication
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
        Template for basic authentication
    """
    def extract_base64_authorization_header(
         self, authorization_header: str) -> str:
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

    def decode_base64_authorization_header(
         self, base64_authorization_header: str) -> str:
        """
            returns the decoded value of base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # change the base64_authorization_header to binary string
            binary_string = base64_authorization_header.encode('utf-8')

            # change the binary_string to binary code
            binary_code = base64.b64decode(binary_string)

            # return the decoded value as a string
            return binary_code.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
         self, decoded_base64_authorization_header: str) -> (str, str):
        """
            return user email and password
            from base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        elif not isinstance(decoded_base64_authorization_header, str):
            return None, None
        elif ':' not in decoded_base64_authorization_header:
            return None, None
        else:
            email = decoded_base64_authorization_header.split(':')[0]
            password = decoded_base64_authorization_header.split(':')[1]
            return email, password
