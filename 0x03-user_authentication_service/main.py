#!/usr/bin/env python3
"""module for validating status codes"""
import requests as rq


base_url = 'http://localhost:5000'


def register_user(email: str, passwd: str) -> None:
    """register a user and create an instance"""
    data = {
        'email': email,
        'password': passwd
    }
    res = rq.post(f'{base_url}/users', data=data)
    status_code = res.status_code
    assert status_code == 200


def log_in(email: str, passwd: str) -> str:
    """login and return session_id"""
    data = {
        'email': email,
        'password': passwd
    }
    res = rq.post(f'{base_url}/sessions', data=data)
    session_id = res.cookies['session_id']
    return session_id


def log_in_wrong_password(email: str, passwd: str) -> None:
    """check that login with wrong password is not possible"""
    data = {
        'email': email,
        'password': passwd
    }
    res = rq.post(f'{base_url}/sessions', data=data)
    status_code = res.status_code
    assert status_code == 401


def profile_unlogged() -> None:
    """check that profile is not logged when wrong credentials entered"""
    res = rq.get(f'{base_url}/profile')
    status_code = res.status_code
    assert status_code == 403


def profile_logged(session_id: str) -> None:
    """return a user profile"""
    cookies = dict(session_id=session_id)
    res = rq.get(f'{base_url}/profile', cookies=cookies)
    status_code = res.status_code
    assert status_code == 200


def log_out(session_id: str) -> None:
    """logout a user"""
    cookies = dict(session_id=session_id)
    res = rq.delete(f'{base_url}/sessions', cookies=cookies)
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """get the password reset token"""
    data = {
        "email": email
    }
    res = rq.post(f'{base_url}/reset_password', data=data)
    data = res.json()
    token = data['reset_token']
    return token


def update_password(email: str, reset_token: str, new_passwd: str) -> None:
    """update a users password"""
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_passwd
    }
    res = rq.put(f'{base_url}/reset_password', data=data)
    status_code = res.status_code
    assert status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
