#!/usr/bin/env python3
"""Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    bpasswd = bytes(password, 'utf-8')
    return bcrypt.hashpw(bpasswd, bcrypt.gensalt())
