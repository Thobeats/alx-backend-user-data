#!/usr/bin/env python3
"""
Session Auth module
"""
from flask import request
from typing import List, TypeVar
import re
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class
    """
