#!/usr/bin/env python3
from .auth import Auth
import base64


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
