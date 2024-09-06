#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
import re
from os import getenv


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication
           checks if a path is in the list of excluded paths
        """

        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p[-1] == '*':
                if re.match(p[:-1], path):
                    return False

            if p[-1] != '/':
                p += '/'
            if re.match(path, p):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
           returns the value of the Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
           returns None
        """
        return None

    def session_cookie(self, request=None):
        """Session cookie
           returns a cookie value from a request
        """
        if request is None:
            return None
        SESSION_NAME = getenv('SESSION_NAME')

        if SESSION_NAME is None:
            return None

        return request.cookies.get(SESSION_NAME)
