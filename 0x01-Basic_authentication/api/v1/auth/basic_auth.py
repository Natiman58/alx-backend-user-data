#!/usr/bin/env python3
"""
    Definition of basic authentication
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def user_object_from_credentials(
         self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            returns a User object
            based on the extracted email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
            if not user or user == []:
                return None
            for i in user:
                if i.is_valid_password(user_pwd):
                    return i
            return None
        except Exception:
            pass

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns the current user based on request
        """
        # Authorize the header
        header_auth = self.authorization_header(request)
        # if header is authenticated and not none
        if header_auth is not None:
            # extract the base64 part of the header
            h_base64 = self.extract_base64_authorization_header(header_auth)
            # if the extracted base64 is not None
            if h_base64 is not None:
                # decode the base64 part of the header
                h_decoded = self.decode_base64_authorization_header(h_base64)
                # if the decoded base64 is not None
                if h_decoded is not None:
                    # extract the user email and pwd
                    email, pwd = self.extract_user_credentials(h_decoded)
                    # if email and pwd aren't none
                    if email is not None and pwd is not None:
                        # get the current user obj using the email and pwd
                        user = self.user_object_from_credentials(email, pwd)
                        # return the current user
                        return user
        else:
            return None
