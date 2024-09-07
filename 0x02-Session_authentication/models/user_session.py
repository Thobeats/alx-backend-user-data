#!/usr/bin/env python3
"""User Session Model"""
from models.base import Base


class UserSession(Base):
    """User session class"""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        setattr(self, 'user_id', kwargs.get('user_id', ""))
        setattr(self, 'session_id', kwargs.get('session_id', ""))
