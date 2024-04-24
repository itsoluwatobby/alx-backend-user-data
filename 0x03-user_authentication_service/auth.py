#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import gensalt, hashpw, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    """This function hashes a password and then returns the
    hashed password

    Argument:
        password<str>: Password to be hashed

    Returns the hashed_password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Generate a uuid using the uuid module

    Returns the generated uuid
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """Create a user session

        Argument:
            email<str>: user email
        Returns a sessionId
        """
        try:
            sessionId = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=sessionId)
            return sessionId
        except NoResultFound as e:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user by the session_id

        Arguments:
            session_id<str>: session_id to find a user

        Returns the user if found or None
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound as e:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session

        Argument:
            user_id<int>: userId
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound as e:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Retrieves the user reset token

        Argument:
            email<str>: user email

        Returns the reset token
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user_id, reset_token=token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user password

        Argument:
            reset_token<str>: reset_token to update user password
            password<str>: new password to replace the previous
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound as e:
            raise ValueError
