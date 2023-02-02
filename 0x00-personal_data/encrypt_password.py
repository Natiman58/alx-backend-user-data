#!/usr/bin/env python3
"""
This script is used to hash passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password
    :param password: password to hash
    return byte strings
    """
    bytes = password.encode('utf-8')  # convert pwd into byte array
    salt = bcrypt.gensalt()  # generate salt
    hash = bcrypt.hashpw(bytes, salt)  # hash password
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password is valid
    :param hashed_password: hashed password
    :param password: password to check
    return boolean
    """
    userpw = password.encode('utf-8')  # encode user pwd into byte array
    return bcrypt.checkpw(userpw, hashed_password)
