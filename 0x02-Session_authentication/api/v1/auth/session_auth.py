#!/usr/bin/env python3
"""
Empty session
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User

class SessionAuth(Auth):
    """An Authentication session class"""
    user_id_by_session_id = {}

    def __init__(self):
        """Initializes an instance of the Session class"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on the session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on the cookie value"""
        session = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(session)

