#!/usr/bin/env python3
"""
Basic Auth module
"""
from flask import request
from typing import List, TypeVar
import re
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """BasicAuth class
    """
