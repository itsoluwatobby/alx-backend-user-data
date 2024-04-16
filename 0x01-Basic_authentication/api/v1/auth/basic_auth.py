#!/usr/bin/env python3
"""
BasicAuth class
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
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
        """A function that extracts authorization_header from
        the request header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
