#!/usr/bin/env python3
"""
Session DB Auth module
"""
from uuid import uuid4
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class
    """

    def __init__(self):
        """Overloads the __init__ method of SessionAuth class"""
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """Create session
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        self.user_id_by_session_id[session_id] = user_session
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for session ID
        """
        if session_id is None:
            return None
        session = UserSession.search({'session_id': session_id})
        if not session:
            return None
        if self.session_duration <= 0:
            return session[0].user_id
        user_session = session[0]
        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expired_time < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        session = UserSession.search({'session_id': session_cookie})
        if not session:
            return False
        session[0].remove()
        return True
