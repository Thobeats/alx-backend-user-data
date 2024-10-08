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

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
            return None
        except (NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


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
