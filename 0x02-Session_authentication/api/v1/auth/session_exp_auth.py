#!/usr/bin/env python3
"""
Session with an Expiration time
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """An Authentication session class"""

    def __init__(self):
        """Initializes an instance of the Session class"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
                        'user_id': user_id,
                        'created_at': datetime.now()
                    }
        SessionAuth.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on the session_id"""
        if session_id is None:
            return None

        user_session = SessionAuth.user_id_by_session_id.get(session_id)
        if not user_session:
            return None
        if self.session_duration <= 0:
            return user_session['user_id']
        if 'created_at' not in user_session:
            return None
        delta = timedelta(seconds=self.session_duration)
        if user_session['created_at'] + delta < datetime.now():
            return None
        return user_session['user_id']
