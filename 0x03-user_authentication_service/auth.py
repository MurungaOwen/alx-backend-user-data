#!/usr/bin/env python3
"""module for authentication"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """hashes the password using bcrypt"""
    byted_pwd = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byted_pwd, bcrypt.gensalt(14))
    return hashed_password


def _generate_uuid():
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """class constructor for auth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user and returns a user instance"""
        try:
            user_found = self._db.find_user_by(email=email)
            if user_found:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_passwd = _hash_password(password)
            added_user = self._db.add_user(email, hashed_passwd)
            return added_user

    def valid_login(self, email: str, password: str) -> bool:
        """checks whether the email and password is valid for login
        :returns - True if valid login
        """
        try:
            user = self._db.find_user_by(email=email)
            passwd_match = bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
            )
            return True if passwd_match and user else False
        except NoResultFound or InvalidRequestError:
            return False

    def create_session(self, email: str) -> str:
        """creates a sessionn for user
        - finds the user corresponding to the email
        generate UUID and store it in the database as session_id
        - :returns - session Id
        """
        try:
            user = self._db.find_user_by(email=email)
            user_id = user.id
            session_id = _generate_uuid()
            self._db.update_user(user_id, session_id=session_id)
            return session_id
        except NoResultFound or InvalidRequestError:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get User based on session_id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound or InvalidRequestError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy a users session"""
        try:
            user = self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound or InvalidRequestError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """set a token to be used when passwd is forgotten"""
        user = self._db.find_user_by(email=email)
        if user:
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            return reset_token
        else:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update a password by using reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_pwd,
                reset_token=None
            )
        except InvalidRequestError or NoResultFound:
            raise ValueError
