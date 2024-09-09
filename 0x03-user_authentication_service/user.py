#!/usr/bin/env python3
"""User class module."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """User Class"""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    string = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)
