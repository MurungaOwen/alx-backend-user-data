#!/usr/bin/env python3
"""module for session expiry authentication
"""
from .session_auth import SessionAuth
from models.user import User
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """class that makes a session expire after a time"""
    def __init__(self):
        """initialise the class or like a constructor for the class"""
        session_duration_str = os.getenv("SESSION_DURATION", "0")
        try:
            self.session_duration = int(session_duration_str)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session"""
        create_session = super().create_session()
        session_id = create_session if create_session else None
        user_id_by_session_id = super().user_id_by_session_id
        session_dictionary = {
            'user_id': user_id_by_session_id,
            'created_at': datetime.now()
        }
        user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user id based on session id as long as session hasnt expired"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict["user_id"]
        created_at = session_dict["created_at"]
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return session_dict["user_id"]
