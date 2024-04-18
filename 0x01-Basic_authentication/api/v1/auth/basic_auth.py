#!/usr/bin/env python3
"""
module for the basic authentication
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """this defines the basic authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract base64 from the headers provided
        """
        auth = authorization_header
        is_string = (type(auth) is str) if auth else None
        starts_by_basic = (auth.startswith('Basic' + ' ')) \
            if is_string else None
        if auth:
            if is_string and starts_by_basic:
                encode_string = auth[len("Basic "):]
                return encode_string
            return None
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode the base 64 we get from header"""
        b64 = base64_authorization_header
        if b64:
            if isinstance(b64, str):
                try:
                    decoded_bytes = base64.b64decode(b64)
                    decoded_string = decoded_bytes.decode('utf-8')
                    return decoded_string
                except base64.binascii.Error:
                    return None
            return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extracting credentials provided by user
        :return
            :user email
            :user password
        """
        decoded_b64 = decoded_base64_authorization_header
        if decoded_b64:
            if isinstance(decoded_base64_authorization_header, str):
                first_colon_index = decoded_b64.find(':')
                if first_colon_index != -1:
                    email = decoded_b64[:first_colon_index]
                    password = decoded_b64[first_colon_index + 1:]
                    return email, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """getting user from credentials that were set
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None
        users = User.search({"email": user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns who the curret user is"""
        header = self.authorization_header(request)
        extracted_info = self.extract_base64_authorization_header(header)
        decoded_info = self.decode_base64_authorization_header(extracted_info)
        user_cred = self.extract_user_credentials(decoded_info)
        username, email = user_cred
        user = self.user_object_from_credentials(username, email)
        return user
