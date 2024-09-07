#!/usr/bin/env python3
"""
Session Expiry Auth module
"""
from uuid import uuid4
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    
    def __init__(self):
        """Overloads the __init__ method of SessionAuth class"""
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """Create session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for session ID
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id].get("user_id")
        session_dictionary = self.user_id_by_session_id[session_id]
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        total_time = created_at.timestamp() + self.session_duration
        if total_time < datetime.now().timestamp():
            return None
        return session_dictionary.get("user_id")
        