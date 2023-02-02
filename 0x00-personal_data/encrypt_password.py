#!/usr/bin/env python3
"""
This script is used to hash passwords.
"""
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password
    :param password: password to hash
    return bytes
    """
    bytes = password.encode('utf-8')  # convert pwd into byte array
    salt = bcrypt.gensalt()  # generate salt
    hash = bcrypt.hashpw(bytes, salt)  # hash password
    return hash
