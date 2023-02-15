#!/usr/bin/env python3
"""
    a script to hash a password
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
        hash the password using
    """
    # convert the password str into bytes
    bytes = password.encode('utf-8')
    # generate the salt
    salt = bcrypt.gensalt()
    # generte the hashed pwd
    hash = bcrypt.hashpw(bytes, salt)
    # return the pwd
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            if the user is not in the database
            register the user and return the user object
        """
        try:
            # Try to find the user with the given email
            self._db.find_user_by(email=email)

            # is the user already registered, raise a ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # if the user is not registered, hash the password
            hashed_pwd = _hash_password(password)

            # then create a new user with the given email and hashed pwd
            new_user = self._db.add_user(email, hashed_pwd)

            # return the new user
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
            Validate the login credentials for a user.
            Args:
            email (str): The email of the user.
            password (str): The password of the user.
            Returns:
            bool: True if the login is successful, False otherwise.
        """
        try:
            # locating the user by email
            user = self._db.find_user_by(email=email)
            # if it exists check if the pwd matches the hashed pwd
            # if so; return True
            return bcrypt.checkpw(
                                  password.encode('utf-8'),
                                  user.hashed_password
                                  )

        # if no user was found return False
        except NoResultFound:
            return False

    def _generate_uuid() -> str:
        """
            A private method to generate uuid
            and return the string format of the uuid
        """
        return str(uuid.uuid4())
