#!/usr/bin/env python3
"""
Encryption of password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """expects string -> name and password. It returns
       a salted-hashed password.

    Arguments:
        password(str): password

    Returns:
        bytes: encryption password
    """
    if password:
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks for password validity

    Args:
        hashed_password (bytes): hash
        password (str): password

    Returns:
        bool: true or false
    """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)
