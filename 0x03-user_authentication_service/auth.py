#!/usr/bin/env python3
"""
    a script to hash a password
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """
        hash the password using 
    """
    # convert the password str into bytes
    bytes = password.encode('utf-8')
    # generate the salt string
    salt = bcrypt.gensalt()
    # generte the hashed pwd
    hash = bcrypt.hashpw(bytes, salt)
    # return the pwd
    return hash
