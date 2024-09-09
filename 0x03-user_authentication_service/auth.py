#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        return self._db.add_user(email, _hash_password(password))


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    bpasswd = bytes(password, 'utf-8')
    return bcrypt.hashpw(bpasswd, bcrypt.gensalt())
