#!/usr/bin/env python3
"""module for session authentication
"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """the session auth class and its working"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session for a user based on credentials
        :return
            - session id
        """
        if user_id and isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user id based on session id"""
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """return user instance based on cookie value"""
        cookie = self.session_cookie(request)
        print(f'{cookie} is cookie')
        user_id = str(self.user_id_for_session_id(cookie))
        print(f"user id: {user_id}")
        if user_id:
            user = User.get(user_id)
            return user
        return None
