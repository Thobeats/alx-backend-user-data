#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login Credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return False
            return bcrypt.checkpw(bytes(password, 'utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """
        Create a session
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, session_id: str) -> None:
        """
        Destroy a session
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """
    Generate a UUID
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    bpasswd = bytes(password, 'utf-8')
    return bcrypt.hashpw(bpasswd, bcrypt.gensalt())
