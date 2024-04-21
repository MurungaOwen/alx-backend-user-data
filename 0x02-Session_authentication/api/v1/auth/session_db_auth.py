#!/usr/bin/env python3
"""module for session authentication in db
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """sessions in a database"""
    def create_session(self, user_id=None):
        """create a session for a user"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            # Save user_session to the database (file in your case)
            # Example: user_session.save_to_database()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user id based on session id """
        if session_id:
            # Query the database (file) to retrieve user_id based on session_id
            # Example: user_session = UserSession.query_by_session_id
            user_session = None  # Placeholder for database query
            if user_session:
                return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """destroy the session id"""
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                return True  # Placeholder for deletion success
        return False
