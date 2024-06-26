#!/usr/bin/env python3
"""
module for authentication
"""
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch


class Auth:
    """
    Handles the authentication of users
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if we dont need authentication
        :params
            - path ehich is intended url
            - excluded_paths which is paths needing auth
        :return
            - True if we dont need authentication
            - False if we need authentication
        """
        if not path:
            return True

        path = path.rstrip("/")
        if not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path.rstrip('*')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        header that has auth info and identifies use
        :params
            -request
        """
        if request:
            if 'Authorization' not in request.headers:
                return None
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user
        """
        return None
