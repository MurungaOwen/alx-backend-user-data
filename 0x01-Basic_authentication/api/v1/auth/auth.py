#!/usr/bin/env python3
"""
module for authentication
"""
from flask import request
from typing import List, TypeVar


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
        new_path = path.rstrip("/") if path else None
        new_excluded_paths = [p.rstrip('/') for p in excluded_paths] \
            if excluded_paths else None
        if new_path and new_excluded_paths:
            if len(excluded_paths) == 0:
                return True
            if new_path not in new_excluded_paths:
                return True
        elif not new_path | (not new_excluded_paths):
            return True
        else:
            return False

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
