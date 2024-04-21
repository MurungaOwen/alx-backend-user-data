#!/usr/bin/env python3
""" user stored in database"""
from .base import Base

class UserSession(Base):
    """user session in a db"""
    def __init__(self, *args: list, **kwargs: dict):
        """constructor for the class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
