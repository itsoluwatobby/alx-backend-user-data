#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import gensalt, hashpw, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """This function hashes a password and then returns the
    hashed password

    Argument:
        password<str>: Password to be hashed

    Returns the hashed_password
    """
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method that handles user registration"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound as e:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials

        Arguments:
            email<str>: user email address
            password<str>: user password

        Returns a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as e:
            return False
        else:
            return checkpw(password.encode('utf-8'), user.hashed_password)
