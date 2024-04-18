#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """An instance of the Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authenticates a request"""
        if path is None or len(excluded_paths) == 0 or excluded_paths is None:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """A function that attaches headers to the request"""
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Function that gets the current_user"""
        return None

    def session_cookie(self, request=None) -> str:
        """returns a cookie value from the request"""
        try:
            session_name = getenv('SESSION_NAME')
            return request.cookies.get(session_name)
        except ValueError as e:
            return None
