#!/usr/bin/env python3
"""
Session with a Storage db
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """An session db class"""

    def __init__(self):
        """Initializes an instance of the Session db class"""
        super().__init__()

    def create_session(self, user_id=None) -> str:
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns a user_id based on the session_id"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        users = UserSession.search({'session_id': session_id})
        for user in users:
            delta = timedelta(seconds=self.session_duration)
            if user.created_at + delta < datetime.now():
                return None
            return user.user_id

    def destroy_session(self, request=None):
        """Delete the user session / log out
        """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            users = UserSession.search({'session_id': session_id})
            for user in users:
                user.remove()
                UserSession.save_to_file()
                return True
        return False
