#!/usr/bin/env python3
"""
BasicAuth class
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    An instance of the BasicAuth class that inherits from
    the Auth class
    """

    def __init__(self):
        """Instantiates an instance of the BasicAuth class"""
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """A method that extracts authorization_header from
        the request header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """method that decodes a base64 authorization
        header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64.b64decode(base64_authorization_header)
        except Exception as e:
            return None
        else:
            decode_bytes = base64.b64decode(base64_authorization_header)
            return decode_bytes.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """method that extracts the user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        value = decoded_base64_authorization_header.split(':', 1)
        return (value[0], value[1]) if value else (None, None)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """fetches user instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Function that gets the current_user"""
        try:
            header = self.authorization_header(request)
            base64_h = self.extract_base64_authorization_header(header)
            decode_h = self.decode_base64_authorization_header(base64_h)
            credents = self.extract_user_credentials(decode_h)
            return self.user_object_from_credentials(credents[0], credents[1])
        except Exception:
            return None
